================================================================================
  HADOOP CLUSTER START/STOP COMMANDS
================================================================================

All scripts are located at: $HADOOP_HOME/sbin/
On this system:          /home/koushik/bigdata/hadoop/sbin/

--------------------------------------------------------------------------------
  START COMMANDS
--------------------------------------------------------------------------------

# Start ONLY HDFS (NameNode + DataNode + SecondaryNameNode)
$HADOOP_HOME/sbin/start-dfs.sh

# Start ONLY YARN (ResourceManager + NodeManager)
$HADOOP_HOME/sbin/start-yarn.sh

# Start BOTH HDFS and YARN together
$HADOOP_HOME/sbin/start-all.sh

# Start ONLY the NameNode (manual)
$HADOOP_HOME/bin/hdfs --daemon start namenode

# Start ONLY the DataNode (manual)
$HADOOP_HOME/bin/hdfs --daemon start datanode

# Start ONLY the SecondaryNameNode
$HADOOP_HOME/bin/hdfs --daemon start secondarynamenode

# Start ONLY the ResourceManager
$HADOOP_HOME/bin/yarn --daemon start resourcemanager

# Start ONLY the NodeManager
$HADOOP_HOME/bin/yarn --daemon start nodemanager

# Start MapReduce Job History Server
$HADOOP_HOME/bin/mapred --daemon start historyserver

--------------------------------------------------------------------------------
  STOP COMMANDS
--------------------------------------------------------------------------------

# Stop ONLY HDFS
$HADOOP_HOME/sbin/stop-dfs.sh

# Stop ONLY YARN
$HADOOP_HOME/sbin/stop-yarn.sh

# Stop BOTH HDFS and YARN
$HADOOP_HOME/sbin/stop-all.sh

# Stop ONLY the NameNode
$HADOOP_HOME/bin/hdfs --daemon stop namenode

# Stop ONLY the DataNode
$HADOOP_HOME/bin/hdfs --daemon stop datanode

# Stop ONLY the SecondaryNameNode
$HADOOP_HOME/bin/hdfs --daemon stop secondarynamenode

# Stop ONLY the ResourceManager
$HADOOP_HOME/bin/yarn --daemon stop resourcemanager

# Stop ONLY the NodeManager
$HADOOP_HOME/bin/yarn --daemon stop nodemanager

# Stop MapReduce Job History Server
$HADOOP_HOME/bin/mapred --daemon stop historyserver

--------------------------------------------------------------------------------
  CHECK RUNNING PROCESSES
--------------------------------------------------------------------------------

# List all Java processes (Hadoop daemons show up here)
jps

# Expected output when everything is running:
#   12345 NameNode
#   12346 DataNode
#   12347 SecondaryNameNode
#   12348 ResourceManager
#   12349 NodeManager
#   12350 JobHistoryServer
#   12351 Jps

--------------------------------------------------------------------------------
  NAMENODE FORMAT (ONE TIME ONLY!)
--------------------------------------------------------------------------------

# WARNING: Run this ONLY the very first time, or to completely reset HDFS.
# This DELETES all data in HDFS!
hdfs namenode -format

# Format without interactive prompt
hdfs namenode -format -nonInteractive

# Format with a specific cluster ID
hdfs namenode -format -clusterid my-cluster-01

--------------------------------------------------------------------------------
  WEB UI URLS (running on this system)
--------------------------------------------------------------------------------

  HDFS NameNode UI   :  http://localhost:9870
  YARN ResourceManager:  http://localhost:8088
  MapReduce History  :  http://localhost:19888

================================================================================
