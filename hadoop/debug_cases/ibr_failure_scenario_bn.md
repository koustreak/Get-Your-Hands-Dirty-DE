# Debug Case: IBR Fail হলে কি Block হারায়?

> **প্রশ্ন:** DataNode Block-XYZ লিখল কিন্তু Incremental Block Report (IBR) পাঠাতে পারল না — তাহলে কি block হারিয়ে যাবে?  
> **উত্তর:** না। কারণ HDFS-এ **৩টি Safety Net** আছে।

---

## আগে বোঝো — Block ID কে বানায়? NameNode নিজে!

**সবচেয়ে গুরুত্বপূর্ণ কথা:** DataNode কোনো Block ID "আবিষ্কার" করে না।  
**NameNode-ই Block ID generate করে** এবং Client-কে দেয় — লেখা শুরুর আগেই।

```
CLIENT                    NAMENODE                   DATANODE
  │                          │                          │
  │  "foo.txt লিখব,         │                          │
  │   block দরকার"          │                          │
  │ ─────────────────────►  │                          │
  │                          │                          │
  │                    NameNode নিজেই                  │
  │                    Block ID বানায়:                 │
  │                    blk_10000001                    │
  │                    + DN1, DN2, DN3 select করে      │
  │                    + UNDER CONSTRUCTION mark করে   │
  │                          │                          │
  │  "blk_10000001 লেখো,    │                          │
  │   DN1, DN2, DN3-এ"      │                          │
  │ ◄─────────────────────  │                          │
  │                          │                          │
  │  blk_10000001 data ───────────────────────────►   │
  │  pipeline-এ পাঠায়      │   DN1 → DN2 → DN3        │
  │                          │                          │
  │                          │   লেখা শেষ              │
  │                          │  ◄── IBR: "blk_10000001 │
  │  ACK ◄───────────────────────── DN3→DN2→DN1        │
  │                          │   physically আছে" ✅    │
  │                          │                          │
  │  "লেখা শেষ" ──────────► │                          │
  │                          │  UNDER CONSTRUCTION      │
  │                          │       → COMPLETE ✅      │
```

### তাহলে NameNode আগে থেকেই জানে কারণ:

```
Block ID কে বানায়?         → NameNode নিজে
DN select কে করে?          → NameNode নিজে
UNDER CONSTRUCTION কে করে? → NameNode নিজে

DataNode শুধু বলে (IBR-এ):
"তুমি যে blk_10000001 বানিয়েছিলে,
 সেটা আমার কাছে physically আছে, size 128MB, checksum xyz"
```

### NameNode-এর Block Table time অনুযায়ী:

```
① Client request করার আগে:
┌──────────────┬──────────────────┬───────────┐
│ Block ID     │ State            │ DataNodes │
├──────────────┼──────────────────┼───────────┤
│   (খালি)    │                  │           │
└──────────────┴──────────────────┴───────────┘

② Client request করার পর (লেখার আগেই!):
┌──────────────────┬────────────────────┬─────────────┐
│ Block ID         │ State              │ DataNodes   │
├──────────────────┼────────────────────┼─────────────┤
│ blk_10000001     │ UNDER CONSTRUCTION │ DN1,DN2,DN3 │
└──────────────────┴────────────────────┴─────────────┘

③ IBR আসার পর:
┌──────────────────┬──────────┬──────────────────────────┐
│ Block ID         │ State    │ Confirmed on             │
├──────────────────┼──────────┼──────────────────────────┤
│ blk_10000001     │ COMPLETE │ DN1 ✅, DN2 ✅, DN3 ✅   │
└──────────────────┴──────────┴──────────────────────────┘
```

> **IBR-এর আসল কাজ:** Block "planned" থেকে "physically exists" — এই transition confirm করা।  
> NameNode আগে থেকেই জানে block কোথায় থাকার কথা, IBR শুধু physically নিশ্চিত করে।

---

## Scenario: IBR পাঠাতে ব্যর্থ হলো

```
DN1 Block-XYZ লিখল ✅
DN1 IBR পাঠাতে চাইল... ❌ FAILED
```

### কী হবে? — ৩টা Safety Net আছে

---

### 🛡️ Safety Net 1: IBR Queue + Auto Retry

IBR **একটা queue-তে** জমা থাকে। একবার fail করলেই শেষ না —

```
DN1-এর IBR Queue:
┌────────────────────────────┐
│  Block-XYZ → PENDING       │  ← fail হলে এখানেই থাকে
│  Block-ABC → PENDING       │
└────────────────────────────┘
        ↓ retry
        ↓ retry
        ↓ retry (কয়েক সেকেন্ড পর)
     ✅ SUCCESS → NameNode জানল
```

---

### 🛡️ Safety Net 2: Heartbeat-এর সাথে IBR যায়

প্রতি **3 সেকেন্ডে** যে Heartbeat যায়, তার সাথে **pending IBR** গুলোও পাঠানো হয়:

```
config: dfs.blockreport.incremental.intervalMsec = 300 (default)

3 সেকেন্ড পর → Heartbeat পাঠাচ্ছে
                + সাথে pending Block-XYZ IBR ✅
```

মানে, IBR আলাদাভাবে fail করলেও পরের **heartbeat-এই** চলে যাবে।

---

### 🛡️ Safety Net 3: NameNode আগে থেকেই জানে (UNDER CONSTRUCTION)

```
NameNode-ই Block ID বানিয়েছে, তাই সে জানে:
blk_10000001 → UNDER CONSTRUCTION → DN1, DN2, DN3
      ↑
  লেখা শুরুর আগেই এই entry ছিল!

IBR না এলেও NameNode জানে:
  - block-টা কোন DN-এ থাকার কথা
  - কী ID দিয়ে তৈরি হয়েছে

IBR শুধু confirm করে: "DN1-এর disk-এ physically আছে" ✅
```

> 💡 **মনে রাখো:** IBR fail মানে NameNode অন্ধ হয়ে যাওয়া না —  
> সে আগে থেকেই সব plan জানে, IBR শুধু execution confirm করে।

---

## Worst Case: IBR fail + DN crash হলে কী হয়?

```
Block-XYZ DN1-এ লেখা হলো
IBR fail করতে থাকল
DN1 crash করল  ← এখন সমস্যা!
```

**এই case-এ কী হবে:**

```
NameNode দেখছে: Block-XYZ → UNDER CONSTRUCTION

Client-এর কাছে ACK গেছে?

  না গেলে → Client-এ Write Error → Client আবার চেষ্টা করবে

  গেলে (DN2, DN3 ঠিকঠাক) →
    NameNode দেখবে DN2, DN3 থেকে IBR এসেছে
    DN1 dead → block DN2, DN3-এ আছে → re-replicate করবে
    Block-XYZ safe ✅
```

---

## সবচেয়ে Worst Case

```
DN1, DN2, DN3 সবাই Block-XYZ লিখল
সবার IBR fail করল
সবাই crash করল

→ DN তিনটা restart হলে Full Block Report পাঠাবে
→ NameNode: "ও! Block-XYZ এদের কাছে আছে" → reconcile ✅

কিন্তু যদি Disk নষ্ট হয়ে যায় তিনটারই →
→ ❌ Data Loss (এটা hardware failure, software দিয়ে ঠেকানো যায় না)
```

---

## কখন Data হারায়, কখন হারায় না

```
কখন data হারায় না:
✅ IBR fail      → retry হয়, heartbeat-এ যায়
✅ DN crash      → অন্য DN-এ replicated copy থাকে
✅ DN restart    → Full Block Report-এ সব জানায়

কখন data হারায়:
❌ Replication factor-এর সব DN-এর disk একসাথে physically নষ্ট
❌ Single node + replication=1 → DN crash = data gone
```

---

## Related Configs

| Config | File | Default | কাজ |
|--------|------|---------|-----|
| `dfs.blockreport.incremental.intervalMsec` | `hdfs-site.xml` | `300ms` | IBR পাঠানোর interval |
| `dfs.heartbeat.interval` | `hdfs-site.xml` | `3s` | Heartbeat interval (IBR-ও বহন করে) |
| `dfs.blockreport.intervalMsec` | `hdfs-site.xml` | `21600000ms` (6 ঘণ্টা) | Full Block Report interval |

---

## সারসংক্ষেপ

> **IBR failure মানে data loss না।**  
> IBR শুধু একটু দেরিতে NameNode-কে জানাবে, কিন্তু জানাবেই —  
> কারণ retry queue, heartbeat, এবং UNDER CONSTRUCTION state তিনটাই backup হিসেবে কাজ করে।  
> Data তখনই হারায় যখন **সব replication copy-র hardware একসাথে নষ্ট হয়।**
