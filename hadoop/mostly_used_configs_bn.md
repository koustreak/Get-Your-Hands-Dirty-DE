# Hadoop — সবচেয়ে বেশি ব্যবহৃত Configurations (বাংলায়)

> Real-world Hadoop cluster setup বা tuning করতে গেলে যে configurations সবচেয়ে বেশি লাগে — সেগুলোর practical guide।  
> প্রতিটি config-এর সাথে **কেন লাগে**, **কখন বদলাতে হয়** এবং **recommended value** দেওয়া আছে।

---

## 📌 Category অনুযায়ী Index

| # | Category | কী নিয়ে |
|---|----------|---------|
| 1 | [Setup & Connection](#1-setup--connection) | NameNode address, filesystem |
| 2 | [Storage & Disk](#2-storage--disk) | Data directory, block size |
| 3 | [Replication](#3-replication) | Data safety, copy count |
| 4 | [Memory & Performance](#4-memory--performance) | JVM heap, container memory |
| 5 | [Heartbeat & Timeout](#5-heartbeat--timeout) | Node alive check |
| 6 | [Safemode](#6-safemode) | Startup behavior |
| 7 | [Job & Task](#7-job--task) | MapReduce job tuning |
| 8 | [Logging](#8-logging) | Log retention |
| 9 | [Pseudo-Distributed Mode](#9-pseudo-distributed-one-machine-setup) | Single machine setup |

---

## 1. Setup & Connection

### `fs.defaultFS` ⭐⭐⭐⭐⭐
```xml
<!-- File: core-site.xml -->
<property>
  <name>fs.defaultFS</name>
  <value>hdfs://localhost:9000</value>
</property>
```
| | |
|--|--|
| **কাজ** | Hadoop কোন NameNode-এ connect করবে |
| **কখন বদলায়** | প্রতিটি fresh setup-এ দিতেই হয় |
| **Dev value** | `hdfs://localhost:9000` |
| **Prod value** | `hdfs://master-node.company.com:9000` |
| **না দিলে** | Hadoop local filesystem ব্যবহার করে, HDFS কাজ করে না |

---

### `hadoop.tmp.dir` ⭐⭐⭐⭐
```xml
<!-- File: core-site.xml -->
<property>
  <name>hadoop.tmp.dir</name>
  <value>/opt/hadoop/tmp</value>
</property>
```
| | |
|--|--|
| **কাজ** | NameNode, DataNode সব temporary data এখানে রাখে |
| **কখন বদলায়** | Setup-এ একবার, `/tmp` avoid করতে |
| **⚠️ সতর্কতা** | `/tmp` দিলে reboot-এ সব data যাবে — NameNode corrupt হবে |

---

## 2. Storage & Disk

### `dfs.namenode.name.dir` ⭐⭐⭐⭐⭐
```xml
<!-- File: hdfs-site.xml -->
<property>
  <name>dfs.namenode.name.dir</name>
  <value>file:///opt/hadoop/data/namenode</value>
</property>
```
| | |
|--|--|
| **কাজ** | NameNode তার FSImage ও EditLog এখানে রাখে |
| **কখন বদলায়** | প্রতিটি setup-এ দিতেই হয় |
| **Prod tip** | Multiple path দাও — `file:///disk1/nn,file:///disk2/nn` (redundancy) |
| **⚠️ সতর্কতা** | এই directory corrupt হলে পুরো HDFS নষ্ট হয় |

---

### `dfs.datanode.data.dir` ⭐⭐⭐⭐⭐
```xml
<!-- File: hdfs-site.xml -->
<property>
  <name>dfs.datanode.data.dir</name>
  <value>file:///opt/hadoop/data/datanode</value>
</property>
```
| | |
|--|--|
| **কাজ** | DataNode HDFS block এখানে store করে |
| **কখন বদলায়** | প্রতিটি setup-এ দিতেই হয় |
| **Prod tip** | প্রতিটি disk আলাদা path দাও — `file:///disk1/dn,file:///disk2/dn,file:///disk3/dn` |
| **Performance** | Multiple disk দিলে parallel write হয়, throughput বাড়ে |

---

### `dfs.blocksize` ⭐⭐⭐
```xml
<!-- File: hdfs-site.xml -->
<property>
  <name>dfs.blocksize</name>
  <value>134217728</value>  <!-- 128 MB -->
</property>
```
| | |
|--|--|
| **কাজ** | HDFS-এ file store হওয়ার সময় কত size-এ block split হবে |
| **Default** | 128 MB |
| **Large file (GB/TB)** | 256MB বা 512MB দাও → কম block, কম NameNode memory |
| **Small file (KB)** | 64MB দাও → ব্যবধান কমে |
| **MapReduce** | ১টি block = ১টি Map task (সাধারণত) |

---

## 3. Replication

### `dfs.replication` ⭐⭐⭐⭐⭐
```xml
<!-- File: hdfs-site.xml -->
<property>
  <name>dfs.replication</name>
  <value>3</value>
</property>
```
| | |
|--|--|
| **কাজ** | প্রতিটি block কতটি DataNode-এ copy হবে |
| **Single node** | `1` দিতেই হবে, না দিলে warning আসে |
| **Production** | `3` (industry standard) |
| **কম দিলে** | ডেটা হারানোর risk বাড়ে |
| **বেশি দিলে** | Disk space বেশি লাগে, write slow হয় |

---

## 4. Memory & Performance

### `yarn.nodemanager.resource.memory-mb` ⭐⭐⭐⭐⭐
```xml
<!-- File: yarn-site.xml -->
<property>
  <name>yarn.nodemanager.resource.memory-mb</name>
  <value>8192</value>  <!-- 8 GB -->
</property>
```
| | |
|--|--|
| **কাজ** | একটি NodeManager কত MB memory Container-দের দিতে পারবে |
| **Rule of thumb** | Machine RAM-এর 75-80% দাও |
| **16 GB RAM** | `12288` (12 GB) |
| **32 GB RAM** | `24576` (24 GB) |
| **⚠️ বেশি দিলে** | OS-এর জন্য memory কম থাকে, machine crash করতে পারে |

---

### `yarn.nodemanager.resource.cpu-vcores` ⭐⭐⭐⭐
```xml
<!-- File: yarn-site.xml -->
<property>
  <name>yarn.nodemanager.resource.cpu-vcores</name>
  <value>8</value>
</property>
```
| | |
|--|--|
| **কাজ** | NodeManager কতটি virtual CPU Container-দের দেবে |
| **Rule of thumb** | Physical core-এর সমান বা কম দাও |
| **8 core machine** | `6` বা `8` |

---

### `mapreduce.map.memory.mb` ⭐⭐⭐⭐
```xml
<!-- File: mapred-site.xml -->
<property>
  <name>mapreduce.map.memory.mb</name>
  <value>1024</value>
</property>
```
| | |
|--|--|
| **কাজ** | প্রতিটি Map task Container কত MB পাবে |
| **Default** | 1024 MB |
| **OOM error হলে** | বাড়িয়ে 2048 বা 4096 দাও |
| **সাথে এটাও দাও** | `mapreduce.map.java.opts=-Xmx768m` (75% of memory) |

---

### `mapreduce.reduce.memory.mb` ⭐⭐⭐⭐
```xml
<!-- File: mapred-site.xml -->
<property>
  <name>mapreduce.reduce.memory.mb</name>
  <value>2048</value>
</property>
```
| | |
|--|--|
| **কাজ** | প্রতিটি Reduce task Container কত MB পাবে |
| **Default** | 2048 MB |
| **সাধারণত** | Map-এর দ্বিগুণ দেওয়া ভালো |
| **সাথে এটাও দাও** | `mapreduce.reduce.java.opts=-Xmx1536m` |

---

### `yarn.scheduler.minimum-allocation-mb` + `maximum-allocation-mb` ⭐⭐⭐
```xml
<!-- File: yarn-site.xml -->
<property>
  <name>yarn.scheduler.minimum-allocation-mb</name>
  <value>512</value>
</property>
<property>
  <name>yarn.scheduler.maximum-allocation-mb</name>
  <value>8192</value>
</property>
```
| | |
|--|--|
| **কাজ** | Container-এর memory range define করে |
| **কখন বদলায়** | Map/Reduce memory বাড়ালে maximum-ও বাড়াতে হয় |
| **Rule** | maximum ≤ nodemanager.resource.memory-mb |

---

## 5. Heartbeat & Timeout

### `dfs.heartbeat.interval` ⭐⭐⭐⭐
```xml
<!-- File: hdfs-site.xml -->
<property>
  <name>dfs.heartbeat.interval</name>
  <value>3</value>  <!-- seconds -->
</property>
```
| | |
|--|--|
| **কাজ** | DataNode কত সেকেন্ড পরপর NameNode-কে "alive" signal দেবে |
| **Default** | 3 সেকেন্ড |
| **Network busy হলে** | 5-10 সেকেন্ড করো |
| **Fast failure detection চাইলে** | 1-2 সেকেন্ড (কিন্তু traffic বাড়বে) |

---

### `dfs.namenode.heartbeat.recheck-interval` ⭐⭐⭐
```xml
<!-- File: hdfs-site.xml -->
<property>
  <name>dfs.namenode.heartbeat.recheck-interval</name>
  <value>300000</value>  <!-- 5 minutes in ms -->
</property>
```
| | |
|--|--|
| **কাজ** | NameNode কতক্ষণ heartbeat না পেলে DataNode-কে dead ধরবে |
| **Default** | 5 মিনিট |
| **Prod** | 2-3 মিনিট করা যায় faster recovery-র জন্য |

---

### `yarn.resourcemanager.nodemanagers.heartbeat-interval-ms` ⭐⭐⭐
```xml
<!-- File: yarn-site.xml -->
<property>
  <name>yarn.resourcemanager.nodemanagers.heartbeat-interval-ms</name>
  <value>1000</value>  <!-- 1 second -->
</property>
```
| | |
|--|--|
| **কাজ** | NodeManager কত ms পরপর ResourceManager-কে heartbeat দেবে |
| **Default** | 1000ms = 1 সেকেন্ড |
| **Large cluster** | 500ms করলে faster scheduling |

---

### `mapreduce.task.timeout` ⭐⭐⭐⭐
```xml
<!-- File: mapred-site.xml -->
<property>
  <name>mapreduce.task.timeout</name>
  <value>300000</value>  <!-- 5 minutes -->
</property>
```
| | |
|--|--|
| **কাজ** | কোনো Task এই সময়ে progress না করলে kill হয় |
| **Default** | 5 মিনিট |
| **Heavy computation হলে** | 600000 (10 min) বা বেশি দাও |
| **0 দিলে** | কখনো timeout হবে না (সতর্কতার সাথে ব্যবহার করো) |
| **কখন বাড়াতে হয়** | "Task timeout" error দেখলে |

---

## 6. Safemode

### `dfs.namenode.safemode.threshold-pct` ⭐⭐⭐⭐
```xml
<!-- File: hdfs-site.xml -->
<property>
  <name>dfs.namenode.safemode.threshold-pct</name>
  <value>0.999</value>
</property>
```
| | |
|--|--|
| **কাজ** | DataNode-এর কত % block report এলে NameNode safemode ছাড়বে |
| **Default** | 99.9% |
| **Single node dev** | `0` দাও — সাথে সাথে safemode ছাড়বে |
| **Prod** | 0.999 বা 0.99 |
| **Symptom** | Startup-এ HDFS write fail করলে, safemode-এ আটকা আছে কিনা দেখো |

```bash
# Manually safemode check ও বের হওয়ার command:
hdfs dfsadmin -safemode get
hdfs dfsadmin -safemode leave
```

---

### `dfs.namenode.safemode.min.datanodes` ⭐⭐⭐
```xml
<!-- File: hdfs-site.xml -->
<property>
  <name>dfs.namenode.safemode.min.datanodes</name>
  <value>0</value>
</property>
```
| | |
|--|--|
| **কাজ** | Safemode ছাড়তে minimum কতটি DataNode live থাকতে হবে |
| **Single node** | `0` দাও |
| **3-node cluster** | `1` বা `2` দাও |

---

## 7. Job & Task

### `mapreduce.framework.name` ⭐⭐⭐⭐⭐
```xml
<!-- File: mapred-site.xml -->
<property>
  <name>mapreduce.framework.name</name>
  <value>yarn</value>
</property>
```
| | |
|--|--|
| **কাজ** | MapReduce কোন framework-এ চলবে |
| **yarn** | Production standard — YARN-এর উপরে চলে |
| **local** | Single JVM-এ চলে — debugging-এ কাজে লাগে |
| **না দিলে** | YARN-এ job submit করা যায় না |

---

### `mapreduce.job.reduces` ⭐⭐⭐⭐
```xml
<!-- File: mapred-site.xml (অথবা job submit-এর সময়) -->
<property>
  <name>mapreduce.job.reduces</name>
  <value>1</value>
</property>
```
| | |
|--|--|
| **কাজ** | কতটি Reduce task চলবে |
| **0 দিলে** | Reduce phase হবে না (Map-only job) |
| **Rule of thumb** | `0.95 × (nodes × max_containers_per_node)` |

---

### `mapreduce.map.output.compress` ⭐⭐⭐
```xml
<!-- File: mapred-site.xml -->
<property>
  <name>mapreduce.map.output.compress</name>
  <value>true</value>
</property>
<property>
  <name>mapreduce.map.output.compress.codec</name>
  <value>org.apache.hadoop.io.compress.SnappyCodec</value>
</property>
```
| | |
|--|--|
| **কাজ** | Map → Reduce shuffle-এর সময় data compress হয় |
| **কখন দেবে** | Network slow হলে বা shuffle data বিশাল হলে |
| **Codec** | Snappy (fast) বা LZ4 (faster) — production-এ |

---

## 8. Logging

### `yarn.log-aggregation-enable` ⭐⭐⭐⭐
```xml
<!-- File: yarn-site.xml -->
<property>
  <name>yarn.log-aggregation-enable</name>
  <value>true</value>
</property>
```
| | |
|--|--|
| **কাজ** | Job শেষে Container logs HDFS-এ save হয় |
| **কখন দেবে** | সবসময় — না দিলে failed job debug করা কঠিন |
| **Log দেখার command** | `yarn logs -applicationId <app_id>` |

---

### `yarn.log-aggregation.retain-seconds` ⭐⭐⭐
```xml
<!-- File: yarn-site.xml -->
<property>
  <name>yarn.log-aggregation.retain-seconds</name>
  <value>604800</value>  <!-- 7 days -->
</property>
```
| | |
|--|--|
| **কাজ** | Aggregated log কতদিন HDFS-এ থাকবে |
| **Dev** | 86400 (1 দিন) |
| **Prod** | 604800 (7 দিন) বা বেশি |
| **-1 দিলে** | কখনো delete হবে না (disk full হবে সাবধান) |

---

### `fs.trash.interval` ⭐⭐⭐
```xml
<!-- File: core-site.xml -->
<property>
  <name>fs.trash.interval</name>
  <value>1440</value>  <!-- 24 hours -->
</property>
```
| | |
|--|--|
| **কাজ** | HDFS-এ delete করা ফাইল কতক্ষণ Trash-এ থাকবে |
| **0 দিলে** | Trash বন্ধ — সরাসরি delete (বিপজ্জনক!) |
| **Prod** | 1440 (24 ঘণ্টা) বা 4320 (3 দিন) |

---

## 9. Pseudo-Distributed (One Machine) Setup

> Single machine-এ Hadoop চালানোর জন্য minimum required configs।  
> Interview বা practice-এর জন্য এই setup সবচেয়ে বেশি ব্যবহৃত।

### `core-site.xml`
```xml
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
  </property>
  <property>
    <name>hadoop.tmp.dir</name>
    <value>/opt/hadoop/tmp</value>
  </property>
</configuration>
```

### `hdfs-site.xml`
```xml
<configuration>
  <!-- Single machine, তাই replication = 1 -->
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>file:///opt/hadoop/data/namenode</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>file:///opt/hadoop/data/datanode</value>
  </property>
  <!-- Safemode-এ আটকা না থাকতে -->
  <property>
    <name>dfs.namenode.safemode.threshold-pct</name>
    <value>0</value>
  </property>
</configuration>
```

### `yarn-site.xml`
```xml
<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
  <property>
    <name>yarn.nodemanager.aux-services.mapreduce_shuffle.class</name>
    <value>org.apache.hadoop.mapred.ShuffleHandler</value>
  </property>
  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>localhost</value>
  </property>
</configuration>
```

### `mapred-site.xml`
```xml
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
  <property>
    <name>mapreduce.jobhistory.address</name>
    <value>localhost:10020</value>
  </property>
  <property>
    <name>mapreduce.jobhistory.webapp.address</name>
    <value>0.0.0.0:19888</value>
  </property>
</configuration>
```

---

## 🚨 Common Errors ও Fix

| Error | কারণ | Config Fix |
|-------|------|-----------|
| `Name node is in safe mode` | DataNode কম online | `dfs.namenode.safemode.threshold-pct=0` অথবা `hdfs dfsadmin -safemode leave` |
| `Task killed: task timeout` | Task অনেক time নিচ্ছে | `mapreduce.task.timeout` বাড়াও |
| `Container killed, exceeded memory` | Job-এ memory কম | `mapreduce.map.memory.mb` বাড়াও |
| `Connection refused (9000)` | NameNode চলছে না | `fs.defaultFS` check করো, `start-dfs.sh` দাও |
| `No space left on device` | DataNode disk full | `dfs.datanode.data.dir` নতুন disk add করো |
| `Replica placement failed` | DataNode-এর চেয়ে replication বেশি | `dfs.replication` কমাও বা DataNode বাড়াও |

---

## ⭐ Priority Ranking (কোনটা আগে জানতে হবে)

```
⭐⭐⭐⭐⭐  MUST KNOW
├── fs.defaultFS
├── dfs.replication
├── dfs.namenode.name.dir
├── dfs.datanode.data.dir
├── mapreduce.framework.name
└── yarn.nodemanager.resource.memory-mb

⭐⭐⭐⭐  IMPORTANT
├── hadoop.tmp.dir
├── dfs.heartbeat.interval
├── mapreduce.task.timeout
├── mapreduce.map.memory.mb
├── mapreduce.reduce.memory.mb
└── yarn.log-aggregation-enable

⭐⭐⭐  GOOD TO KNOW
├── dfs.blocksize
├── dfs.namenode.safemode.threshold-pct
├── yarn.nodemanager.resource.cpu-vcores
├── mapreduce.map.output.compress
└── fs.trash.interval
```
