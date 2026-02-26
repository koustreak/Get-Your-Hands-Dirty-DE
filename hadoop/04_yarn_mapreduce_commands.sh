================================================================================
  YARN COMMANDS  (yarn application / yarn node / yarn queue)
================================================================================

--------------------------------------------------------------------------------
  APPLICATION MANAGEMENT
--------------------------------------------------------------------------------

# List all running YARN applications
yarn application -list

# List applications by state (ALL, NEW, RUNNING, FINISHED, FAILED, KILLED)
yarn application -list -appStates RUNNING
yarn application -list -appStates FINISHED
yarn application -list -appStates FAILED

# List by application type (SPARK, MAPREDUCE)
yarn application -list -appTypes SPARK

# Get details of a specific application
yarn application -status application_1234567890_0001

# Kill a running application
yarn application -kill application_1234567890_0001

--------------------------------------------------------------------------------
  APPLICATION LOGS
--------------------------------------------------------------------------------

# Get logs for a completed application
yarn logs -applicationId application_1234567890_0001

# Get logs for a specific container
yarn logs -applicationId application_1234567890_0001 -containerId container_..._01

# Get logs for a specific node
yarn logs -applicationId application_1234567890_0001 -nodeAddress localhost:8042

# Save logs to a file
yarn logs -applicationId application_1234567890_0001 > app_logs.txt

--------------------------------------------------------------------------------
  NODE MANAGEMENT
--------------------------------------------------------------------------------

# List all nodes in the cluster
yarn node -list

# List only RUNNING nodes
yarn node -list -states RUNNING

# List all nodes (even decommissioned)
yarn node -list -all

# Get details of a specific node
yarn node -status localhost:8042

--------------------------------------------------------------------------------
  QUEUE MANAGEMENT
--------------------------------------------------------------------------------

# List all queues
yarn queue -status default

# Check queue status
yarn queue -status root.default

--------------------------------------------------------------------------------
  RESOURCE MANAGER (RM) ADMIN
--------------------------------------------------------------------------------

# Force RM to refresh node list
yarn rmadmin -refreshNodes

# Force RM to refresh queue configs
yarn rmadmin -refreshQueues

# Force RM to refresh user/group mappings
yarn rmadmin -refreshUserToGroupsMappings

# RM HA: get current RM state (ACTIVE or STANDBY)
yarn rmadmin -getServiceState rm1

# RM HA: manually failover
yarn rmadmin -failover rm1 rm2

================================================================================
  MAPREDUCE COMMANDS
================================================================================

# Run a MapReduce job
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
    wordcount /input /output

# List available example jobs
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar

# Run Pi estimation example
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
    pi 10 100

# Check MapReduce job status
mapred job -status job_1234567890_0001

# List all MapReduce jobs
mapred job -list

# Kill a MapReduce job
mapred job -kill job_1234567890_0001

# Get MapReduce job counters
mapred job -counter job_1234567890_0001 "Map-Reduce Framework" "Map input records"

================================================================================
  HDFS OFFLINE TOOLS
================================================================================

# OIV — Offline Image Viewer: Read FSImage in human-readable form
hdfs oiv -i /home/koushik/bigdata/hadoop-data/namenode/current/fsimage_0000000000000000000 \
         -o /tmp/fsimage_output.xml \
         -p XML

# OIV with ReverseXML processor
hdfs oiv -i fsimage_0000000000000000000 -p ReverseXML -o output.xml

# OIV with Web interface (starts a local web server)
hdfs oiv -i fsimage_0000000000000000000 -o /tmp/output -p Web

# OEV — Offline Edit Viewer: Read EditLog in human-readable form
hdfs oev -i /home/koushik/bigdata/hadoop-data/namenode/current/edits_inprogress_0000000000000000003 \
         -o /tmp/edits_output.xml \
         -p xml

# OEV Stats processor (shows edit operation counts)
hdfs oev -i edits_inprogress_0000000000000000003 -p stats

================================================================================
  HADOOP GENERAL UTILITY COMMANDS
================================================================================

# Check Hadoop version
hadoop version

# Check HDFS version
hdfs version

# Check classpath
hadoop classpath

# Verify Hadoop environment variables
hadoop envvars

# Run a Hadoop filesystem shell (interactive)
hadoop fs -ls /          # (same as hdfs dfs -ls /)

# Archive small files into HAR (Hadoop Archive) to reduce NameNode load
hadoop archive -archiveName mydata.har -p /user/koushik /user/koushik/archives

# List files in a HAR archive
hadoop fs -ls har:///user/koushik/archives/mydata.har

================================================================================
