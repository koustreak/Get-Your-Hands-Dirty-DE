# Hadoop Configuration ফাইলসমূহ (বাংলায়)

> **Location:** `$HADOOP_HOME/etc/hadoop/`  
> Hadoop-এর সব configuration XML ফাইল এই directory-তে থাকে।  
> এখানে প্রতিটি ফাইল আলাদা আলাদা component-এর behavior নিয়ন্ত্রণ করে।

---

## 📁 সব Configuration ফাইলের তালিকা

| ফাইল | কোন Component | কাজ কী |
|------|--------------|---------|
| `core-site.xml` | Hadoop Core | FS address, IPC, security |
| `hdfs-site.xml` | HDFS | NameNode, DataNode, replication |
| `yarn-site.xml` | YARN | ResourceManager, NodeManager |
| `mapred-site.xml` | MapReduce | Job history, task timeout |
| `hadoop-env.sh` | সব | JVM, Java path, heap size |
| `yarn-env.sh` | YARN | YARN-এর JVM settings |
| `mapred-env.sh` | MapReduce | MR-এর JVM settings |
| `workers` | সব | Slave/Worker node-এর list |
| `log4j.properties` | সব | Logging configuration |
| `capacity-scheduler.xml` | YARN Scheduler | Queue ও resource allocation |
| `fair-scheduler.xml` | YARN Scheduler | Fair scheduling policy |
| `ssl-server.xml` | Security | SSL/TLS সার্ভার সেটিং |
| `ssl-client.xml` | Security | SSL/TLS ক্লায়েন্ট সেটিং |

---

## 1️⃣ `core-site.xml` — Hadoop Core Configuration

> **কাজ কী?**  
> Hadoop-এর সবচেয়ে মৌলিক settings এখানে থাকে।  
> NameNode-এর address, default filesystem, security, IPC, network timeout — সব কিছু।  
> **hdfs-site.xml, yarn-site.xml সবাই এই ফাইলের উপর নির্ভর করে।**

```xml
<configuration>

  <!-- ======================
       FILESYSTEM SETTINGS
       ====================== -->

  <!-- Default Filesystem: কোন NameNode-এ connect করবে -->
  <!-- hdfs://localhost:9000 মানে localhost-এ port 9000-এ NameNode আছে -->
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
    <description>
      Default filesystem URI. HDFS-এর জন্য hdfs://host:port দিতে হয়।
      এটা না দিলে Hadoop local filesystem ব্যবহার করে।
    </description>
  </property>

  <!-- Hadoop temporary data কোথায় রাখবে -->
  <property>
    <name>hadoop.tmp.dir</name>
    <value>/opt/hadoop/tmp</value>
    <description>
      Temporary ফাইল এবং data এখানে রাখা হয়।
      NameNode এবং DataNode উভয়ই এই path ব্যবহার করে।
      Production-এ /tmp ব্যবহার করা ঠিক না — reboot-এ ডেটা যায়।
    </description>
  </property>

  <!-- ======================
       IPC & NETWORK SETTINGS
       ====================== -->

  <!-- IPC client কতবার connect retry করবে -->
  <property>
    <name>ipc.client.connect.max.retries</name>
    <value>10</value>
    <description>
      Server unavailable হলে client কতবার পুনরায় connect চেষ্টা করবে।
      Default: 10
    </description>
  </property>

  <!-- Retry-র মাঝে কত ms অপেক্ষা করবে -->
  <property>
    <name>ipc.client.connect.retry.interval</name>
    <value>1000</value>
    <description>
      প্রতিটি reconnect attempt-এর মধ্যে বিরতি (milliseconds)।
      Default: 1000ms = 1 সেকেন্ড
    </description>
  </property>

  <!-- IPC connection timeout -->
  <property>
    <name>ipc.client.connect.timeout</name>
    <value>20000</value>
    <description>
      Server-এর সাথে connection establish করতে maximum কত ms লাগতে পারবে।
      Default: 20000ms = 20 সেকেন্ড
    </description>
  </property>

  <!-- Ping interval: connection alive আছে কিনা চেক করে -->
  <property>
    <name>ipc.ping.interval</name>
    <value>5000</value>
    <description>
      RPC connection alive কিনা চেক করার interval (milliseconds)।
      Default: 5000ms = 5 সেকেন্ড
    </description>
  </property>

  <!-- IPC server thread pool size -->
  <property>
    <name>ipc.server.listen.queue.size</name>
    <value>128</value>
    <description>
      IPC server কতটি pending connection queue-তে রাখতে পারবে।
    </description>
  </property>

  <!-- ======================
       SECURITY SETTINGS
       ====================== -->

  <!-- Kerberos authentication চালু/বন্ধ -->
  <property>
    <name>hadoop.security.authentication</name>
    <value>simple</value>
    <description>
      simple = কোনো authentication নেই (Dev/Learning-এর জন্য)
      kerberos = Production-এ Kerberos দিতে হয়
    </description>
  </property>

  <!-- Authorization চালু করা -->
  <property>
    <name>hadoop.security.authorization</name>
    <value>false</value>
    <description>
      true করলে hadoop-policy.xml অনুযায়ী access control হয়।
      Production-এ true রাখা উচিত।
    </description>
  </property>

  <!-- ======================
       TRASH SETTINGS
       ====================== -->

  <!-- HDFS-এ delete করলে trash-এ যাবে কিনা এবং কতক্ষণ থাকবে -->
  <property>
    <name>fs.trash.interval</name>
    <value>1440</value>
    <description>
      Delete হওয়া ফাইল Trash-এ কত মিনিট থাকবে।
      1440 = 24 ঘণ্টা
      0 = Trash বন্ধ (সরাসরি delete)
    </description>
  </property>

  <!-- Trash checkpoint interval -->
  <property>
    <name>fs.trash.checkpoint.interval</name>
    <value>0</value>
    <description>
      Trash checkpoint কত মিনিট পর পর হবে।
      0 মানে fs.trash.interval অনুযায়ী চলবে।
    </description>
  </property>

</configuration>
```

---

## 2️⃣ `hdfs-site.xml` — HDFS Configuration

> **কাজ কী?**  
> HDFS-এর সব ভেতরের কাজ এখানে configure হয়।  
> NameNode কোথায় metadata রাখবে, DataNode কোথায় block রাখবে, replication কত হবে,  
> heartbeat interval কত হবে — সব কিছু এই ফাইলে।

```xml
<configuration>

  <!-- ======================
       REPLICATION SETTINGS
       ====================== -->

  <!-- প্রতিটি block কতটি DataNode-এ replicate হবে -->
  <property>
    <name>dfs.replication</name>
    <value>3</value>
    <description>
      Default replication factor।
      Single node (pseudo-distributed)-এ 1 দিতে হয়।
      Production cluster-এ সাধারণত 3 রাখা হয়।
    </description>
  </property>

  <!-- ======================
       NAMENODE SETTINGS
       ====================== -->

  <!-- NameNode metadata (FSImage, EditLog) কোথায় রাখবে -->
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>file:///opt/hadoop/data/namenode</value>
    <description>
      NameNode তার metadata এই directory-তে রাখে।
      Production-এ multiple path দেওয়া উচিত (comma separated) — redundancy-র জন্য।
      যেমন: file:///disk1/nn,file:///disk2/nn
    </description>
  </property>

  <!-- NameNode HTTP Web UI port -->
  <property>
    <name>dfs.namenode.http-address</name>
    <value>0.0.0.0:9870</value>
    <description>
      NameNode-এর Web UI এই address-এ পাওয়া যায়।
      Browser-এ http://localhost:9870 দিয়ে দেখা যায়।
    </description>
  </property>

  <!-- NameNode RPC port (client connect করে এখানে) -->
  <property>
    <name>dfs.namenode.rpc-address</name>
    <value>localhost:9000</value>
    <description>
      Client এবং DataNode এই port-এ NameNode-এর সাথে কথা বলে।
      core-site.xml-এর fs.defaultFS-এর সাথে match করতে হবে।
    </description>
  </property>

  <!-- ======================
       DATANODE SETTINGS
       ====================== -->

  <!-- DataNode block data কোথায় রাখবে -->
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>file:///opt/hadoop/data/datanode</value>
    <description>
      DataNode তার block data এই directory-তে store করে।
      Multiple disk দিলে throughput বাড়ে:
      file:///disk1/dn,file:///disk2/dn
    </description>
  </property>

  <!-- DataNode HTTP Web UI port -->
  <property>
    <name>dfs.datanode.http.address</name>
    <value>0.0.0.0:9864</value>
    <description>
      DataNode-এর Web UI এই port-এ থাকে।
      http://localhost:9864 দিয়ে দেখা যায়।
    </description>
  </property>

  <!-- ======================
       HEARTBEAT SETTINGS
       ====================== -->

  <!-- DataNode কত সেকেন্ড পরপর NameNode-কে heartbeat পাঠাবে -->
  <property>
    <name>dfs.heartbeat.interval</name>
    <value>3</value>
    <description>
      DataNode প্রতি 3 সেকেন্ডে একবার NameNode-কে জানায় "আমি বেঁচে আছি"।
      এই heartbeat না গেলে NameNode DataNode-কে dead মনে করে।
      কম দিলে network traffic বাড়ে, বেশি দিলে failure detection দেরি হয়।
    </description>
  </property>

  <!-- NameNode কতক্ষণ heartbeat না পেলে DataNode-কে dead ধরবে -->
  <property>
    <name>dfs.namenode.heartbeat.recheck-interval</name>
    <value>300000</value>
    <description>
      NameNode এই interval-এ (milliseconds) DataNode-দের status recheck করে।
      Default: 300000ms = 5 মিনিট।
      একটি DataNode dead হলে এই সময়ের মধ্যে detect হয়।
    </description>
  </property>

  <!-- DataNode কত missed heartbeat-এ stale হবে -->
  <property>
    <name>dfs.namenode.stale.datanode.interval</name>
    <value>30000</value>
    <description>
      একটি DataNode এই সময়ের (ms) মধ্যে heartbeat না দিলে stale বলে mark হয়।
      Stale DataNode-এ নতুন write পাঠানো হয় না।
      Default: 30000ms = 30 সেকেন্ড।
    </description>
  </property>

  <!-- ======================
       BLOCK SETTINGS
       ====================== -->

  <!-- HDFS block size -->
  <property>
    <name>dfs.blocksize</name>
    <value>134217728</value>
    <description>
      প্রতিটি HDFS block-এর default size।
      134217728 bytes = 128 MB।
      Large file processing-এ বড় block efficient।
      ছোট ফাইল বেশি হলে ছোট block (64MB) ভালো।
    </description>
  </property>

  <!-- একটি DataNode কতটি block একসাথে replicate করতে পারবে -->
  <property>
    <name>dfs.datanode.max.transfer.threads</name>
    <value>4096</value>
    <description>
      DataNode একসাথে কতটি block transfer thread চালাতে পারবে।
      বেশি দিলে বেশি concurrent transfer হয় কিন্তু memory বাড়ে।
    </description>
  </property>

  <!-- ======================
       NAMENODE HIGH AVAILABILITY
       ====================== -->

  <!-- Secondary NameNode HTTP address -->
  <property>
    <name>dfs.namenode.secondary.http-address</name>
    <value>0.0.0.0:9868</value>
    <description>
      Secondary NameNode-এর Web UI port।
      Secondary NN, FSImage checkpoint নিয়মিত নেয়।
      HA mode-এ এটার বদলে Standby NameNode ব্যবহার হয়।
    </description>
  </property>

  <!-- FSImage Checkpoint interval (seconds) -->
  <property>
    <name>dfs.namenode.checkpoint.period</name>
    <value>3600</value>
    <description>
      Secondary NameNode কত সেকেন্ড পর পর FSImage checkpoint নেবে।
      Default: 3600 সেকেন্ড = 1 ঘণ্টা।
      বেশি বড় cluster-এ কমানো যায়।
    </description>
  </property>

  <!-- ======================
       PERMISSION SETTINGS
       ====================== -->

  <!-- HDFS permission চেক করবে কিনা -->
  <property>
    <name>dfs.permissions.enabled</name>
    <value>true</value>
    <description>
      true = HDFS Unix-style permission enforce করবে।
      false = সবাই সব কিছু access করতে পারবে (Dev-এ convenient)।
    </description>
  </property>

  <!-- Superuser group নাম -->
  <property>
    <name>dfs.permissions.superusergroup</name>
    <value>supergroup</value>
    <description>
      এই group-এর user সব HDFS path-এ full access পাবে।
    </description>
  </property>

  <!-- ======================
       SAFEMODE SETTINGS
       ====================== -->

  <!-- NameNode safemode-এ কত % block report এলে বের হবে -->
  <property>
    <name>dfs.namenode.safemode.threshold-pct</name>
    <value>0.999</value>
    <description>
      NameNode startup-এ safemode-এ থাকে।
      মোট block-এর 99.9% DataNode থেকে report পেলে safemode ছাড়বে।
      Single node-এ 0 দিলে সাথে সাথে safemode ছাড়ে।
    </description>
  </property>

</configuration>
```

---

## 3️⃣ `yarn-site.xml` — YARN Configuration

> **কাজ কী?**  
> YARN (Yet Another Resource Negotiator) হলো Hadoop-এর resource management layer।  
> কোন job কতটুকু CPU/Memory পাবে, NodeManager কোথায় থাকবে,  
> ResourceManager-এর address কী — এই সব এখানে configure হয়।

```xml
<configuration>

  <!-- ======================
       RESOURCEMANAGER SETTINGS
       ====================== -->

  <!-- ResourceManager hostname -->
  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>localhost</value>
    <description>
      ResourceManager কোন machine-এ চলছে তার hostname।
      Cluster-এ এটা master node-এর hostname হবে।
    </description>
  </property>

  <!-- ResourceManager Web UI address -->
  <property>
    <name>yarn.resourcemanager.webapp.address</name>
    <value>0.0.0.0:8088</value>
    <description>
      YARN-এর Web UI এই port-এ পাওয়া যায়।
      http://localhost:8088 দিয়ে running jobs দেখা যায়।
    </description>
  </property>

  <!-- ResourceManager-এর RPC address -->
  <property>
    <name>yarn.resourcemanager.address</name>
    <value>localhost:8032</value>
    <description>
      Client এই address-এ job submit করে।
    </description>
  </property>

  <!-- Scheduler address -->
  <property>
    <name>yarn.resourcemanager.scheduler.address</name>
    <value>localhost:8030</value>
    <description>
      ApplicationMaster এই address-এ resource request করে।
    </description>
  </property>

  <!-- ======================
       NODEMANAGER SETTINGS
       ====================== -->

  <!-- NodeManager-এ কত memory থাকবে (MB) -->
  <property>
    <name>yarn.nodemanager.resource.memory-mb</name>
    <value>8192</value>
    <description>
      প্রতিটি NodeManager কত MB memory Container-দের দিতে পারবে।
      Machine-এর মোট RAM-এর 80% দেওয়া ভালো।
      8192 = 8 GB।
    </description>
  </property>

  <!-- NodeManager-এ কত virtual CPU core থাকবে -->
  <property>
    <name>yarn.nodemanager.resource.cpu-vcores</name>
    <value>8</value>
    <description>
      NodeManager কতটি virtual CPU core Container-দের দিতে পারবে।
      Machine-এর physical core-এর সংখ্যার সমান বা কম দেওয়া উচিত।
    </description>
  </property>

  <!-- ======================
       HEARTBEAT SETTINGS
       ====================== -->

  <!-- NodeManager কত ms পরপর ResourceManager-কে heartbeat দেবে -->
  <property>
    <name>yarn.resourcemanager.nodemanagers.heartbeat-interval-ms</name>
    <value>1000</value>
    <description>
      NodeManager প্রতি 1 সেকেন্ডে ResourceManager-কে status জানায়।
      কম দিলে faster failure detection, বেশি network traffic।
      বেশি দিলে slow detection, কম traffic।
    </description>
  </property>

  <!-- NodeManager কতক্ষণ heartbeat না দিলে dead ধরবে -->
  <property>
    <name>yarn.nm.liveness-monitor.expiry-interval-ms</name>
    <value>600000</value>
    <description>
      একটি NodeManager এই সময়ের (ms) মধ্যে heartbeat না দিলে dead।
      Default: 600000ms = 10 মিনিট।
    </description>
  </property>

  <!-- ======================
       CONTAINER SETTINGS
       ====================== -->

  <!-- Container-এর minimum memory -->
  <property>
    <name>yarn.scheduler.minimum-allocation-mb</name>
    <value>512</value>
    <description>
      একটি Container সর্বনিম্ন কত MB memory পাবে।
      এর চেয়ে কম request করা যাবে না।
    </description>
  </property>

  <!-- Container-এর maximum memory -->
  <property>
    <name>yarn.scheduler.maximum-allocation-mb</name>
    <value>8192</value>
    <description>
      একটি Container সর্বোচ্চ কত MB memory পাবে।
      yarn.nodemanager.resource.memory-mb-এর বেশি দেওয়া যাবে না।
    </description>
  </property>

  <!-- Container-এর minimum CPU -->
  <property>
    <name>yarn.scheduler.minimum-allocation-vcores</name>
    <value>1</value>
    <description>একটি Container সর্বনিম্ন 1 vcore পাবে।</description>
  </property>

  <!-- Container-এর maximum CPU -->
  <property>
    <name>yarn.scheduler.maximum-allocation-vcores</name>
    <value>4</value>
    <description>একটি Container সর্বোচ্চ 4 vcore পাবে।</description>
  </property>

  <!-- ======================
       NODEMANAGER AUX SERVICES
       ====================== -->

  <!-- MapReduce-এর জন্য shuffle service চালু করা -->
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
    <description>
      MapReduce job চালাতে হলে এই service চালু রাখতেই হবে।
      Map output shuffle হয় এই service-এর মাধ্যমে।
    </description>
  </property>

  <property>
    <name>yarn.nodemanager.aux-services.mapreduce_shuffle.class</name>
    <value>org.apache.hadoop.mapred.ShuffleHandler</value>
    <description>Shuffle service-এর Java class।</description>
  </property>

  <!-- ======================
       LOG SETTINGS
       ====================== -->

  <!-- Container log aggregation চালু করা -->
  <property>
    <name>yarn.log-aggregation-enable</name>
    <value>true</value>
    <description>
      true করলে Container-এর logs HDFS-এ aggregate হয়।
      Job শেষ হলেও logs দেখা যায়।
    </description>
  </property>

  <!-- Aggregated log কতদিন রাখবে -->
  <property>
    <name>yarn.log-aggregation.retain-seconds</name>
    <value>86400</value>
    <description>
      Aggregated logs কত সেকেন্ড রাখবে।
      86400 = 24 ঘণ্টা।
      -1 দিলে কখনো delete হবে না।
    </description>
  </property>

</configuration>
```

---

## 4️⃣ `mapred-site.xml` — MapReduce Configuration

> **কাজ কী?**  
> MapReduce job কীভাবে চলবে তা এখানে define করা হয়।  
> Job History Server কোথায় থাকবে, task timeout কত হবে,  
> Map ও Reduce task-এর memory কত হবে — এই সব এখানে।

```xml
<configuration>

  <!-- ======================
       FRAMEWORK SETTINGS
       ====================== -->

  <!-- MapReduce কোন framework-এ চলবে -->
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
    <description>
      yarn = YARN-এর উপরে MapReduce চলবে (production standard)।
      local = Single JVM-এ চলবে (debugging-এর জন্য)।
      classic = পুরনো MRv1 (Hadoop 1.x) framework।
    </description>
  </property>

  <!-- ======================
       JOB HISTORY SERVER
       ====================== -->

  <!-- Job History Server address -->
  <property>
    <name>mapreduce.jobhistory.address</name>
    <value>localhost:10020</value>
    <description>
      Job History Server-এর RPC address।
      Completed job-এর information এখান থেকে পাওয়া যায়।
    </description>
  </property>

  <!-- Job History Server Web UI -->
  <property>
    <name>mapreduce.jobhistory.webapp.address</name>
    <value>0.0.0.0:19888</value>
    <description>
      Job History-র Web UI।
      http://localhost:19888 দিয়ে past jobs দেখা যায়।
    </description>
  </property>

  <!-- ======================
       TASK SETTINGS
       ====================== -->

  <!-- Task timeout: কোনো task কতক্ষণ progress না করলে kill হবে -->
  <property>
    <name>mapreduce.task.timeout</name>
    <value>300000</value>
    <description>
      একটি Task এই সময়ের (ms) মধ্যে কোনো progress না করলে kill হয়ে যাবে।
      Default: 300000ms = 5 মিনিট।
      Long running task-এ বাড়িয়ে দিতে হবে।
      0 দিলে কখনো timeout হবে না।
    </description>
  </property>

  <!-- ======================
       MEMORY SETTINGS (Map Task)
       ====================== -->

  <!-- Map task Container-এর memory -->
  <property>
    <name>mapreduce.map.memory.mb</name>
    <value>1024</value>
    <description>
      প্রতিটি Map task Container কত MB memory পাবে।
      YARN-এ request হয় এই পরিমাণে।
      yarn.scheduler.minimum-allocation-mb-এর গুণিতক হতে হবে।
    </description>
  </property>

  <!-- Map task JVM heap size -->
  <property>
    <name>mapreduce.map.java.opts</name>
    <value>-Xmx768m</value>
    <description>
      Map task-এর JVM heap size।
      mapreduce.map.memory.mb-এর 75-80% দেওয়া ভালো।
      বাকিটা JVM overhead-এর জন্য।
    </description>
  </property>

  <!-- ======================
       MEMORY SETTINGS (Reduce Task)
       ====================== -->

  <!-- Reduce task Container-এর memory -->
  <property>
    <name>mapreduce.reduce.memory.mb</name>
    <value>2048</value>
    <description>
      প্রতিটি Reduce task Container কত MB memory পাবে।
      Reduce task সাধারণত Map-এর চেয়ে বেশি memory নেয়।
    </description>
  </property>

  <!-- Reduce task JVM heap size -->
  <property>
    <name>mapreduce.reduce.java.opts</name>
    <value>-Xmx1536m</value>
    <description>
      Reduce task-এর JVM heap size।
      mapreduce.reduce.memory.mb-এর 75% এর মতো দেওয়া উচিত।
    </description>
  </property>

  <!-- ======================
       PARALLELISM SETTINGS
       ====================== -->

  <!-- একটি Job-এ কতটি Map task চলবে (hint, override করা যায়) -->
  <property>
    <name>mapreduce.job.maps</name>
    <value>2</value>
    <description>
      Default Map task সংখ্যা। Input split অনুযায়ী automatically ঠিক হয়।
      এটা একটা hint মাত্র, actual value ভিন্ন হতে পারে।
    </description>
  </property>

  <!-- একটি Job-এ কতটি Reduce task চলবে -->
  <property>
    <name>mapreduce.job.reduces</name>
    <value>1</value>
    <description>
      Default Reduce task সংখ্যা।
      0 দিলে Reduce phase চলবে না (Map-only job)।
    </description>
  </property>

  <!-- ======================
       INTERMEDIATE DATA SETTINGS
       ====================== -->

  <!-- Map output compress করবে কিনা -->
  <property>
    <name>mapreduce.map.output.compress</name>
    <value>false</value>
    <description>
      true করলে Map output shuffle-এর সময় compress হয়।
      Network bandwidth বাঁচে কিন্তু CPU বেশি লাগে।
    </description>
  </property>

  <!-- Compression codec -->
  <property>
    <name>mapreduce.map.output.compress.codec</name>
    <value>org.apache.hadoop.io.compress.SnappyCodec</value>
    <description>
      Map output compress করার codec।
      Snappy: fast, কম compression ratio।
      GZip: slow, বেশি compression ratio।
    </description>
  </property>

</configuration>
```

---

## 5️⃣ `hadoop-env.sh` — Environment Variables

> **কাজ কী?**  
> Hadoop-এর সব component-এর JVM settings, Java path, log directory, heap size  
> এই shell script-এ থাকে। XML ফাইল না, কিন্তু equally important।

```bash
# Java installation path
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Hadoop home directory
export HADOOP_HOME=/opt/hadoop

# Hadoop configuration directory
export HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop

# Log files কোথায় যাবে
export HADOOP_LOG_DIR=${HADOOP_HOME}/logs

# PID files কোথায় থাকবে
export HADOOP_PID_DIR=/tmp

# NameNode heap size
export HADOOP_NAMENODE_OPTS="-Xmx2048m -XX:+UseG1GC"

# DataNode heap size
export HADOOP_DATANODE_OPTS="-Xmx1024m"

# Secondary NameNode heap size
export HADOOP_SECONDARYNAMENODE_OPTS="-Xmx2048m"
```

---

## 6️⃣ `yarn-env.sh` — YARN Environment Variables

```bash
# ResourceManager heap size
export YARN_RESOURCEMANAGER_OPTS="-Xmx2048m"

# NodeManager heap size
export YARN_NODEMANAGER_OPTS="-Xmx1024m"

# YARN log directory
export YARN_LOG_DIR=${HADOOP_HOME}/logs
```

---

## 7️⃣ `workers` (পুরনো নাম: `slaves`)

> **কাজ কী?**  
> Hadoop cluster-এ কোন কোন machine DataNode ও NodeManager চালাবে তার list।  
> `start-dfs.sh` এবং `start-yarn.sh` এই ফাইল পড়ে SSH করে সব node চালু করে।

```
# প্রতি লাইনে একটি worker node-এর hostname বা IP
worker1.example.com
worker2.example.com
worker3.example.com
192.168.1.101
192.168.1.102
```

---

## 8️⃣ `capacity-scheduler.xml` — YARN Queue Configuration

> **কাজ কী?**  
> Multiple team বা project-এর জন্য cluster resource ভাগ করে দেওয়া।  
> যেমন: Data Engineering টিম 60% resource পাবে, Data Science টিম 40% পাবে।

```xml
<configuration>
  <property>
    <name>yarn.scheduler.capacity.root.queues</name>
    <value>default,engineering,datascience</value>
    <description>Root queue-এর children queue-গুলোর নাম।</description>
  </property>

  <!-- Engineering queue: 60% resource -->
  <property>
    <name>yarn.scheduler.capacity.root.engineering.capacity</name>
    <value>60</value>
  </property>

  <!-- Data Science queue: 40% resource -->
  <property>
    <name>yarn.scheduler.capacity.root.datascience.capacity</name>
    <value>40</value>
  </property>

  <!-- Engineering queue maximum: burst করলে 80% পর্যন্ত নিতে পারবে -->
  <property>
    <name>yarn.scheduler.capacity.root.engineering.maximum-capacity</name>
    <value>80</value>
  </property>
</configuration>
```

---

## 🔢 গুরুত্বপূর্ণ Default Ports

| Service | Port | কাজ |
|---------|------|-----|
| NameNode RPC | `9000` | Client ও DataNode connect করে |
| NameNode Web UI | `9870` | HDFS ব্রাউজ করা যায় |
| DataNode Web UI | `9864` | DataNode status দেখা যায় |
| Secondary NameNode | `9868` | Checkpoint service |
| ResourceManager Web UI | `8088` | Running jobs দেখা যায় |
| ResourceManager RPC | `8032` | Job submit হয় |
| NodeManager Web UI | `8042` | Container logs দেখা যায় |
| Job History Server | `19888` | Past jobs দেখা যায় |

---

## ⚡ Quick Reference: Heartbeat সংক্রান্ত সব Config

| Property | ফাইল | Default | কাজ |
|----------|------|---------|-----|
| `dfs.heartbeat.interval` | `hdfs-site.xml` | `3s` | DataNode → NameNode heartbeat |
| `dfs.namenode.heartbeat.recheck-interval` | `hdfs-site.xml` | `5 min` | NameNode dead node recheck |
| `dfs.namenode.stale.datanode.interval` | `hdfs-site.xml` | `30s` | DataNode stale threshold |
| `yarn.resourcemanager.nodemanagers.heartbeat-interval-ms` | `yarn-site.xml` | `1000ms` | NodeManager → RM heartbeat |
| `yarn.nm.liveness-monitor.expiry-interval-ms` | `yarn-site.xml` | `10 min` | NodeManager dead threshold |
| `ipc.ping.interval` | `core-site.xml` | `5000ms` | IPC connection alive check |

---

## 🎯 কোন Scenario-তে কোন Config?

### 🐌 Job অনেক slow হচ্ছে
→ `mapred-site.xml` → Map/Reduce memory বাড়াও

### 💾 DataNode disk full হয়ে যাচ্ছে
→ `hdfs-site.xml` → `dfs.datanode.data.dir`-এ নতুন disk add করো

### 🔁 NameNode বারবার safemode-এ ঢুকছে
→ `hdfs-site.xml` → `dfs.namenode.safemode.threshold-pct` কমাও

### ⏱️ Task timeout-এ fail হচ্ছে
→ `mapred-site.xml` → `mapreduce.task.timeout` বাড়াও

### 🖧 Network busy, DataNode অনেক বেশি heartbeat পাঠাচ্ছে
→ `hdfs-site.xml` → `dfs.heartbeat.interval` বাড়াও (5-10 সেকেন্ড)

### 👥 Multiple team-এর job একসাথে চলছে
→ `capacity-scheduler.xml` → Queue-ভিত্তিক resource ভাগ করো
