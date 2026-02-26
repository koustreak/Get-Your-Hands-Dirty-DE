================================================================================
  HDFS ADMIN COMMANDS  (hdfs dfsadmin)
================================================================================

These commands are used by cluster administrators to monitor and manage HDFS.

--------------------------------------------------------------------------------
  CLUSTER HEALTH & MONITORING
--------------------------------------------------------------------------------

# Full cluster health report (live/dead nodes, capacity, blocks)
hdfs dfsadmin -report

# Show only live DataNodes
hdfs dfsadmin -report -live

# Show only dead DataNodes
hdfs dfsadmin -report -dead

# Show only decommissioning DataNodes
hdfs dfsadmin -report -decommissioning

# Get the status of the NameNode
hdfs dfsadmin -metasave metadata_dump.txt

--------------------------------------------------------------------------------
  SAFEMODE
--------------------------------------------------------------------------------
# NOTE: Safe Mode = NameNode is read-only. No writes allowed.
#       HDFS enters Safe Mode automatically on startup until
#       enough blocks are reported by DataNodes.

# Check if HDFS is in safe mode
hdfs dfsadmin -safemode get

# Enter safe mode manually
hdfs dfsadmin -safemode enter

# Leave safe mode manually
hdfs dfsadmin -safemode leave

# Wait until HDFS exits safe mode (useful in scripts)
hdfs dfsadmin -safemode wait

--------------------------------------------------------------------------------
  DATANODE MANAGEMENT
--------------------------------------------------------------------------------

# Refresh the list of hosts (workers file)
hdfs dfsadmin -refreshNodes

# Decommission a DataNode (graceful removal)
# Step 1: Add hostname to $HADOOP_HOME/etc/hadoop/dfs.hosts.exclude
# Step 2: Run refresh
hdfs dfsadmin -refreshNodes
# Step 3: Wait for decommission to complete (check -report)

# Recommission (re-add) a DataNode
# Step 1: Remove hostname from dfs.hosts.exclude
# Step 2: Run refresh
hdfs dfsadmin -refreshNodes

--------------------------------------------------------------------------------
  BALANCER
--------------------------------------------------------------------------------
# If data is unevenly distributed across DataNodes, use the balancer.

# Run the HDFS Balancer (redistributes blocks evenly)
hdfs balancer

# Run balancer with a specific threshold (default 10%)
hdfs balancer -threshold 5

--------------------------------------------------------------------------------
  BLOCK MANAGEMENT
--------------------------------------------------------------------------------

# Trigger a block report from all DataNodes immediately
hdfs dfsadmin -triggerBlockReport

# Run the FSCK (File System Check) on the entire HDFS
hdfs fsck /

# FSCK on a specific directory
hdfs fsck /user/koushik/data/

# FSCK with detailed block information
hdfs fsck / -files -blocks -locations

# FSCK to find and list corrupt files
hdfs fsck / -list-corruptfileblocks

# FSCK to find missing blocks
hdfs fsck / -blocks | grep "MISSING"

--------------------------------------------------------------------------------
  QUOTA MANAGEMENT
--------------------------------------------------------------------------------

# Set name quota (max number of files/dirs)
hdfs dfsadmin -setQuota 1000 /user/koushik

# Clear name quota
hdfs dfsadmin -clrQuota /user/koushik

# Set space quota (in bytes)
hdfs dfsadmin -setSpaceQuota 10g /user/koushik

# Clear space quota
hdfs dfsadmin -clrSpaceQuota /user/koushik

# Check quota usage
hdfs dfs -count -q -h /user/koushik

--------------------------------------------------------------------------------
  ROLLING UPGRADE (Advanced)
--------------------------------------------------------------------------------

# Start rolling upgrade
hdfs dfsadmin -rollingUpgrade prepare

# Check rolling upgrade status
hdfs dfsadmin -rollingUpgrade query

# Finalize the rolling upgrade
hdfs dfsadmin -rollingUpgrade finalize

================================================================================
