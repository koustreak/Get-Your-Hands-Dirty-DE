# HDFS Data Storage Internals (বাংলায়)

> HDFS-এ ডেটা কীভাবে স্টোর হয়, তার একদম ভেতরের গল্প (Disk level)।
> ডেটা কীভাবে ব্লকে ভাঙে, Checksum কীভাবে কাজ করে এবং Directory Structure কেমন হয় তা এখানে বিস্তারিত আলোচনা করা হলো।

---

## ১. HDFS-এ ডেটা কীভাবে ভাঙে? (File → Block → Chunk)

HDFS একটি বড় ফাইলকে সরাসরি রাখে না, ৩টি স্তরে ভেঙে রাখে:

```
  FILE (e.g., video.mp4 - 500 MB)
   │
   ├──▶ BLOCK 1 (128 MB)  --> blk_10000001
   │       │
   │       ├──▶ Chunk 1 (512 bytes) + Checksum (4 bytes)
   │       ├──▶ Chunk 2 (512 bytes) + Checksum (4 bytes)
   │       └──▶ ... (সর্বমোট 262,144 টি Chunk)
   │
   ├──▶ BLOCK 2 (128 MB)  --> blk_10000002
   ├──▶ BLOCK 3 (128 MB)  --> blk_10000003
   └──▶ BLOCK 4 (116 MB)  --> blk_10000004
```

### কেন এভাবে ভাঙে?
1. **Block (128 MB):** বড় ব্লক মানে NameNode-কে কম ব্লকের হিসাব রাখতে হবে। এতে NameNode-এর RAM বাঁচে (প্রতিটি ব্লকের হিসাব রাখতে NameNode-এর আনুমানিক 150 bytes RAM লাগে)।
2. **Chunk (512 Bytes):** পুরো 128 MB ব্লকের একটি মাত্র Checksum বানালে, কোথাও ১ বিট করাপ্ট হলেও পুরো 128 MB ফেলে দিতে হতো। তাই 512 Bytes এর ছোট ছোট Chunk করে Checksum রাখা হয়।

---

## ২. DataNode-এর ডিস্কে ফাইলটা দেখতে কেমন?

DataNode তার লোকাল ফাইল সিস্টেমে (Linux/Ext4/XFS) ডেটাগুলো রাখে।
Directory Structure টা ঠিক এরকম হয়:

```bash
/opt/hadoop/data/datanode/                  <-- dfs.datanode.data.dir
└── current/
    └── BP-531238910-192.168.1.10-161000/   <-- Block Pool ID (প্রতিটি NameNode-এর একটি ইউনিক ID)
        └── current/
            └── finalized/
                │
                ├── subdir0/
                │   ├── blk_10000001              <-- মূল ডেটা (128 MB)
                │   ├── blk_10000001_1001.meta    <-- Checksum ফাইল (প্রায় 1 MB)
                │   ├── blk_10000002
                │   └── blk_10000002_1002.meta
                │
                └── subdir1/                      <-- একটি ফোল্ডারে বেশি ফাইল হলে নতুন ফোল্ডার তৈরি হয়
                    ├── blk_10000050
                    └── blk_10000050_1050.meta
```

**এখানে লক্ষ্য করার বিষয়:**
* NameNode-এর কাছে `video.mp4` নামটা আছে।
* DataNode-এর কাছে `video.mp4` বলে কিছু নেই, তার কাছে শুধু `blk_...` আছে।
* প্রতিটি `blk_` ফাইলের সাথে একটি `_xxxx.meta` ফাইল থাকে, যেখানে ওই ব্লকের Generation Stamp এবং Checksum থাকে।

---

## ৩. `.meta` ফাইলের ভেতরে কী থাকে? (Data Integrity)

HDFS ডেটা করাপ্ট হওয়া থেকে বাঁচাতে Checksum ব্যবহার করে। এই Checksum গুলো `.meta` ফাইলে থাকে।

### `.meta` ফাইলের স্ট্রাকচার:
```
┌────────────────────────────────────────┐
│  Version (2 bytes)                     │
│  Checksum Type: CRC32C (1 byte)        │
│  Bytes per checksum: 512 (4 bytes)     │  <-- dfs.bytes-per-checksum
├────────────────────────────────────────┤
│  Chunk-1 (byte 0-511)    → CRC32C: a1b2│
│  Chunk-2 (byte 512-1023) → CRC32C: c3d4│
│  Chunk-3 (byte 1024-1535)→ CRC32C: e5f6│
│  ...                                   │
│  Chunk-N                 → CRC32C: xxxx│
└────────────────────────────────────────┘
```

**হিসাব:**
* Block Size = 128 MB
* Chunk Size = 512 Bytes
* প্রতিটি Chunk এর CRC32C Checksum = 4 Bytes
* তাহলে পুরো ব্লকের Checksum সাইজ = `(128 MB / 512 Bytes) * 4 Bytes` ≈ `1 MB`
* অর্থাৎ, প্রতিটি 128 MB ব্লকের জন্য 1 MB সাইজের একটি `.meta` ফাইল তৈরি হয়!

---

## ৪. Checksum কীভাবে কাজ করে? (Data Read Flow)

যখন কোনো ক্লায়েন্ট HDFS থেকে ডেটা পড়ে, তখন সে DataNode থেকে সরাসরি ডেটা এবং চেক্সাম দুটোই নেয়:

```
[Client]                                         [DataNode]
   │                                                 │
   │------------- 1. Data Request (blk_x) ---------->│
   │                                                 │
   │<------------ 2. Sends Chunk + Checksum ---------│
   │                                                 │
[Client calculates]
CRC32(Chunk data)
   │
[Client compares]
Calculated CRC == Received Checksum?
   │
   ├── ✅ Match -> Process data
   │
   └── ❌ Missmatch -> Data Corrupted!
               │
               ├──> 1. Client discards the chunk
               ├──> 2. Client reports to NameNode: "DN1's blk_x is corrupt!"
               └──> 3. Client reads from another replica (DN2)
```

**Background Scanner:**
DataNode বসে থাকে না। সে ব্যাকগ্রাউন্ডে `DataBlockScanner` নামের একটি থ্রেড চালায়। এই থ্রেডটি প্রতি ৩ সপ্তাহ (বা কনফিগারেশন অনুযায়ী) অন্তত একবার নিজের ডিস্কের সব ব্লকের Checksum মিলিয়ে দেখে। কোনো ব্লক করাপ্টেড পেলে সে সাথে সাথে NameNode-কে রিপোর্ট করে।

---

## ৫. Generation Stamp (`_1001`) কী?

তুমি খেয়াল করেছ `.meta` ফাইলের নাম `blk_10000001_1001.meta` হয়। এই `1001` হলো **Generation Stamp (GS)**।

**কেন লাগে?**
ধরো, নেটওয়ার্ক ইস্যুর কারণে একটি DataNode কিছুক্ষণের জন্য বিচ্ছিন্ন হয়ে গেল। সেই সময়ে Client ব্লকটির ডেটা আপডেট করল (Append)।
* নতুন ব্লকের GS হবে => `1002` (অন্য DataNode গুলোতে)।
* পুরোনো DataNode ফিরে এলে সে NameNode-কে বলবে: "আমার কাছে `blk_10000001` আছে, যার GS `1001`"।
* NameNode দেখবে, লেটেস্ট GS তো `1002`। তার মানে এই DataNode-এর কাছে পুরোনো (Stale) ডেটা আছে।
* তখন NameNode সেই DataNode-কে ওই পুরোনো ব্লক মুছে ফেলতে বলবে।

Generation Stamp ব্লকের ভার্সন কন্ট্রোল হিসেবে কাজ করে।

---

## ৬. NameNode vs DataNode রেসপনসিবিলিটি

| কাজের ধরন | NameNode | DataNode |
|------------|----------|----------|
| ফাইলের নাম (`video.mp4`) | জানে ✅ | জানে না ❌ |
| কোন ব্লকের ID কী | জানে ✅ (Block ID বানায় সে নিজেই) | জানে ✅ |
| Block ID কোন DN-এ আছে | জানে ✅ | নিজেরগুলো জানে ✅ |
| ফাইলের সাইজ কত | জানে ✅ | জানে না ❌ |
| Checksum / Data Integrity | মাথা ঘামায় না ❌ | সব চেক করে সে নিজেই ✅ |
| Generation Stamp | Track করে ✅ | Store করে `.meta` ফাইলে ✅ |

## সারসংক্ষেপ:
* **ডেটা কীভাবে থাকে:** HDFS ফাইলকে Block-এ ভাঙে, DataNode সেই Block-কে লোকাল Linux File System-এ `blk_xxx` নামে সেভ করে।
* **ফাইল কোথায়:** `dfs.datanode.data.dir`-এর ভেতরে `current/BP-xxx/current/finalized/` পাথে।
* **Integrity:** প্রতি 512 বাইট ডেটার জন্য একটি Checksum তৈরি হয়, যা `.meta` ফাইলে থাকে।
* **Verification:** ডেটা পড়ার সময় Client নিজে Checksum ভেরিফাই করে, এবং DataNode ব্যাকগ্রাউন্ড স্ক্যানার দিয়ে নিয়মিত চেক করে।
