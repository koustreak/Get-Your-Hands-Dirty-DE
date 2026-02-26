# NameNode এবং DataNode — আমার সিস্টেমের ভেতরে কী আছে?

> এই ডকুমেন্টে আমার নিজের মেশিনে চলমান HDFS ক্লাস্টারের সব ফাইল এবং তাদের গভীর ব্যাখ্যা দেওয়া আছে।
> সিস্টেম: `dotpy.com` | তারিখ: February 26, 2026

---

## সম্পূর্ণ ডিরেক্টরি স্ট্রাকচার

```
/home/koushik/bigdata/hadoop-data/
│
├── namenode/                          ← NameNode-এর স্টোরেজ
│   ├── in_use.lock                    ← NameNode চলছে তার প্রমাণ
│   └── current/
│       ├── VERSION                    ← ক্লাস্টারের পরিচয়পত্র
│       ├── seen_txid                  ← শেষ Transaction ID
│       ├── fsimage_0000000000000000000     ← প্রথম FSImage (format-এর সময়)
│       ├── fsimage_0000000000000000000.md5 ← তার Checksum
│       ├── fsimage_0000000000000000014     ← সর্বশেষ Checkpoint-এর FSImage
│       ├── fsimage_0000000000000000014.md5 ← তার Checksum
│       ├── edits_0000000000000000001-0000000000000000002  ← Completed EditLog
│       ├── edits_0000000000000000003-0000000000000000014  ← Completed EditLog
│       └── edits_inprogress_0000000000000000015           ← চলমান EditLog (এখনো শেষ হয়নি)
│
├── datanode/                          ← DataNode-এর স্টোরেজ
│   ├── in_use.lock                    ← DataNode চলছে তার প্রমাণ
│   └── current/
│       ├── VERSION                    ← DataNode-এর পরিচয়পত্র
│       └── BP-129162871-127.0.1.1-1772101145578/   ← Block Pool ডিরেক্টরি
│           ├── scanner.cursor         ← Block Scanner কতদূর এসেছে
│           └── current/
│               └── VERSION           ← Block Pool-এর VERSION
│
└── tmp/                               ← Secondary NameNode-এর কাজের জায়গা
    └── dfs/
        └── namesecondary/
            ├── in_use.lock
            └── current/
                ├── VERSION
                ├── fsimage_0000000000000000002.md5
                ├── fsimage_0000000000000000002     ← SNN-এর তৈরি Checkpoint
                ├── fsimage_0000000000000000014     ← সর্বশেষ SNN Checkpoint
                ├── fsimage_0000000000000000014.md5
                ├── edits_0000000000000000001-0000000000000000002
                └── edits_0000000000000000003-0000000000000000014
```

---

## ১. NameNode-এর ফাইলগুলোর বিস্তারিত বিশ্লেষণ

### 📄 VERSION ফাইল

এটি ক্লাস্টারের **পরিচয়পত্র** — NameNode চালু হওয়ার সময় এটি পড়ে নিজের পরিচয় যাচাই করে।

```properties
# আমার সিস্টেমের আসল VERSION ফাইল
namespaceID  = 1983837745
blockpoolID  = BP-129162871-127.0.1.1-1772101145578
storageType  = NAME_NODE
cTime        = 1772101145578
clusterID    = CID-464722e0-cb17-4762-b940-477e9cbc8261
layoutVersion = -67
```

**প্রতিটি ভ্যালুর মানে কী?**

| ক্ষেত্র | মান | ব্যাখ্যা |
|---|---|---|
| `namespaceID` | `1983837745` | NameNode Format-এর সময় র‍্যান্ডম তৈরি হওয়া নাম্বার। DataNode-কে এই নাম্বার মিলিয়ে দেখতে হয়। |
| `clusterID` | `CID-464722...` | পুরো ক্লাস্টারের ইউনিক পরিচয়। সব নোডে এটি একই থাকে। |
| `blockpoolID` | `BP-129162871...` | এই NameNode-এর Block Pool। DataNode-ও একই ID রেফার করে। |
| `storageType` | `NAME_NODE` | এই ডিরেক্টরিটি NameNode-এর জন্য। |
| `layoutVersion` | `-67` | ডেটার ফরম্যাট ভার্সন। Hadoop upgrade-এ এটি বদলায়। |

---

### 📄 FSImage ফাইল

FSImage হলো HDFS-এর **সম্পূর্ণ স্ন্যাপশট** — সব ফাইল, ডিরেক্টরি, পারমিশন, ব্লক ম্যাপিং একটি বাইনারি ফাইলে সংরক্ষিত।

**আমার সিস্টেমে দুটো FSImage আছে:**

| ফাইল | Transaction ID | সাইজ | কখন তৈরি |
|---|---|---|---|
| `fsimage_0000000000000000000` | 0 (খালি) | 402 bytes | Format করার সময় |
| `fsimage_0000000000000000014` | 14 | 558 bytes | Secondary NameNode Checkpoint করার পরে |

> **আকর্ষণীয় তথ্য:** ফাইলের নামের শেষে সংখ্যাটি হলো **Transaction ID**। এর মানে এই FSImage-টি Transaction-14 পর্যন্ত সব পরিবর্তন ধারণ করে।

**FSImage পড়তে (মানুষের পাঠযোগ্যভাবে):**
```bash
hdfs oiv \
  -i /home/koushik/bigdata/hadoop-data/namenode/current/fsimage_0000000000000000014 \
  -o /tmp/fsimage.xml \
  -p XML
```

---

### 📄 EditLog ফাইল

EditLog হলো HDFS-এর **Transaction Log** — NameNode চালু হওয়ার পর প্রতিটি পরিবর্তন (mkdir, delete, rename, put) এখানে ক্রমানুসারে লেখা হয়।

**আমার সিস্টেমে তিনটি EditLog আছে:**

| ফাইল | TxID Range | সাইজ | অর্থ |
|---|---|---|---|
| `edits_0000000000000000001-0000000000000000002` | 1 → 2 | 42 bytes | Tx-1 থেকে Tx-2 (Closed) |
| `edits_0000000000000000003-0000000000000000014` | 3 → 14 | 1010 bytes | Tx-3 থেকে Tx-14 (Closed) |
| `edits_inprogress_0000000000000000015` | 15 → ? | **1.0 MB** | Tx-15 থেকে এখন পর্যন্ত (চলমান) |

> **আকর্ষণীয় তথ্য:** `edits_inprogress` ফাইলটি **1 MB** কিন্তু ভেতরে মাত্র কয়েক bytes ডেটা আছে। কারণ Hadoop এই ফাইলটি আগেই **Pre-allocate** করে রাখে যাতে ডিস্কে বারবার জায়গা চাইতে না হয় — এটি একটি পারফর্মেন্স অপটিমাইজেশন।

**EditLog পড়তে (মানুষের পাঠযোগ্যভাবে):**
```bash
hdfs oev \
  -i /home/koushik/bigdata/hadoop-data/namenode/current/edits_inprogress_0000000000000000015 \
  -o /tmp/edits.xml \
  -p xml
```

---

### 📄 seen_txid ফাইল

এটি একটি ছোট্ট ফাইল, মাত্র ১-২ bytes — কিন্তু অত্যন্ত গুরুত্বপূর্ণ।

**আমার সিস্টেমে এর মান: `15`**

এর মানে NameNode সর্বশেষ Transaction-15 পর্যন্ত প্রসেস করেছে। NameNode যখন রিস্টার্ট হয়, সে এই ফাইল দেখে জানতে পারে তাকে কোন Transaction ID থেকে EditLog পড়া শুরু করতে হবে।

---

### 🔒 in_use.lock ফাইল

এটি একটি **লক ফাইল**। NameNode চালু থাকলে এই ফাইলটি থাকে।

এটি দুটো কাজ করে:
1. একই ডিরেক্টরিতে দুটো NameNode প্রসেস চালু হওয়া ঠেকায়।
2. অপ্রত্যাশিত শাটডাউনের পরে বোঝা যায় যে NameNode ক্র্যাশ করেছিল।

---

## ২. DataNode-এর ফাইলগুলোর বিস্তারিত বিশ্লেষণ

### 📄 DataNode VERSION ফাইল

```properties
# আমার DataNode-এর আসল VERSION ফাইল
datanodeUuid = 3e3621ee-9eaa-40b7-81d8-974608a020d7
storageType  = DATA_NODE
cTime        = 0
clusterID    = CID-464722e0-cb17-4762-b940-477e9cbc8261
layoutVersion = -57
storageID    = DS-d52186f7-06d3-40fa-952f-9b05f4cddb38
```

| ক্ষেত্র | মান | ব্যাখ্যা |
|---|---|---|
| `datanodeUuid` | `3e3621ee-...` | এই DataNode-এর ইউনিক পরিচয়। NameNode এই UUID দিয়ে DataNode চেনে। |
| `storageID` | `DS-d52186f7...` | এই নির্দিষ্ট ডিস্কের পরিচয়। একটি DataNode-এ একাধিক ডিস্ক থাকতে পারে। |
| `clusterID` | `CID-464722...` | NameNode-এর clusterID-এর সাথে মিলতে হবে, নইলে DataNode রিজেক্ট হবে। |

---

### 📁 Block Pool ডিরেক্টরি

```
BP-129162871-127.0.1.1-1772101145578/
```

এই ডিরেক্টরির নামটি সরাসরি NameNode-এর `blockpoolID` থেকে এসেছে। এটি মিললেই DataNode বুঝতে পারে সে সঠিক ক্লাস্টারের সাথে যুক্ত।

নামের বিভাগ:
- `BP` → Block Pool
- `129162871` → র‍্যান্ডম নাম্বার
- `127.0.1.1` → NameNode-এর IP যখন Format হয়েছিল
- `1772101145578` → Format-এর Unix Timestamp (milliseconds)

---

### 📄 scanner.cursor ফাইল

DataNode-এ একটি **Block Scanner** সার্ভিস চলে যা প্রতিটি ব্লকের Checksum যাচাই করে দেখে ডেটা ঠিকঠাক আছে কিনা। `scanner.cursor` ফাইলে সেভ থাকে শেষবার কোন ব্লক পর্যন্ত স্ক্যান হয়েছে।

---

## ৩. Secondary NameNode (SNN) কীভাবে কাজ করছে তার প্রমাণ

**আমার সিস্টেমে পরিষ্কার প্রমাণ আছে যে SNN কাজ করেছে:**

**NameNode-এ:**
- `edits_0000000000000000001-0000000000000000002` (Closed)
- `edits_0000000000000000003-0000000000000000014` (Closed)
- `fsimage_0000000000000000014` (নতুন Checkpoint তৈরি হয়েছে)

**SNN-এর কাছেও একই ফাইলগুলো আছে:**
```
tmp/dfs/namesecondary/current/
├── fsimage_0000000000000000014
├── fsimage_0000000000000000014.md5
├── edits_0000000000000000001-0000000000000000002
└── edits_0000000000000000003-0000000000000000014
```

**এই থেকে বোঝা যায় Checkpointing ঘটেছে:**
1. SNN NameNode থেকে `fsimage_0` এবং `edits_1-2` নিয়ে এসেছে।
2. Merge করে `fsimage_2` তৈরি করেছে।
3. আবার `edits_3-14` মার্জ করে `fsimage_14` বানিয়েছে।
4. সেই নতুন `fsimage_14` NameNode-কে ফিরিয়ে দিয়েছে।
5. তাই এখন NameNode-এও `fsimage_14` আছে।

---

## ৪. সহজ সারসংক্ষেপ — একটি রিড করার সময় কী হয়?

1. আপনি `hdfs dfs -cat /user/koushik/file.csv` চালালেন।
2. NameNode RAM থেকে দেখে `file.csv`-এর ব্লকগুলো DataNode-এর কোন ডিরেক্টরিতে আছে।
3. সেই DataNode-এর `finalized/subdir0/subdir0/blk_XXXX` ফাইলটি সরাসরি আপনার কাছে পাঠানো হয়।
4. NameNode মাঝখানে আর থাকে না।
