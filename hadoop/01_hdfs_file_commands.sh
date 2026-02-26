================================================================================
  HDFS FILE SYSTEM COMMANDS  (hdfs dfs -<command>)
================================================================================

All commands follow the pattern:
    hdfs dfs -<command> [options] <path>

--------------------------------------------------------------------------------
  DIRECTORY OPERATIONS
--------------------------------------------------------------------------------

# Create a directory
hdfs dfs -mkdir /user/koushik

# Create directory and all parent directories (like mkdir -p)
hdfs dfs -mkdir -p /user/koushik/data/raw

# List files and directories
hdfs dfs -ls /

# List recursively (all subdirectories)
hdfs dfs -ls -R /user/koushik

# Delete an empty directory
hdfs dfs -rmdir /user/koushik/empty_dir

# Delete a directory and all its contents (CAREFUL!)
hdfs dfs -rm -r /user/koushik/old_data

# Delete without moving to trash
hdfs dfs -rm -r -skipTrash /user/koushik/old_data

--------------------------------------------------------------------------------
  FILE OPERATIONS
--------------------------------------------------------------------------------

# Upload a local file to HDFS
hdfs dfs -put /local/path/file.csv /user/koushik/data/

# Upload multiple files
hdfs dfs -put /local/path/*.csv /user/koushik/data/

# Copy from local (same as put)
hdfs dfs -copyFromLocal /local/path/file.csv /user/koushik/data/

# Download a file from HDFS to local
hdfs dfs -get /user/koushik/data/file.csv /local/path/

# Download to local (same as get)
hdfs dfs -copyToLocal /user/koushik/data/file.csv /local/path/

# Move a local file to HDFS (deletes local after upload)
hdfs dfs -moveFromLocal /local/path/file.csv /user/koushik/data/

# Copy file within HDFS
hdfs dfs -cp /user/koushik/data/file.csv /user/koushik/backup/

# Move file within HDFS
hdfs dfs -mv /user/koushik/data/file.csv /user/koushik/archive/

# Delete a file
hdfs dfs -rm /user/koushik/data/file.csv

# Append local file content to an existing HDFS file
hdfs dfs -appendToFile /local/path/new_data.csv /user/koushik/data/file.csv

--------------------------------------------------------------------------------
  FILE VIEWING
--------------------------------------------------------------------------------

# Print file contents to terminal (like cat)
hdfs dfs -cat /user/koushik/data/file.csv

# Print first N lines (like head)
hdfs dfs -cat /user/koushik/data/file.csv | head -20

# Print last N lines (like tail)
hdfs dfs -cat /user/koushik/data/file.csv | tail -20

# Print file contents with paging
hdfs dfs -text /user/koushik/data/file.gz   # also handles compressed files

# Count files, directories, and bytes in a path
hdfs dfs -count /user/koushik/data/

# Show disk usage of files (human readable)
hdfs dfs -du -h /user/koushik/data/

# Show total disk usage summary
hdfs dfs -du -s -h /user/koushik/data/

--------------------------------------------------------------------------------
  FILE INFORMATION
--------------------------------------------------------------------------------

# Check if a file or directory exists (exit code 0 = exists)
hdfs dfs -test -e /user/koushik/data/file.csv

# Check if path is a file
hdfs dfs -test -f /user/koushik/data/file.csv

# Check if path is a directory
hdfs dfs -test -d /user/koushik/

# Show file checksum (MD5/CRC)
hdfs dfs -checksum /user/koushik/data/file.csv

# Show detailed stats of a file
hdfs dfs -stat /user/koushik/data/file.csv

# Show stat with format: %b=bytes, %n=name, %r=replication, %o=blocksize
hdfs dfs -stat "%b %n %r %o" /user/koushik/data/file.csv

# Get file permissions
hdfs dfs -ls /user/koushik/data/

--------------------------------------------------------------------------------
  PERMISSIONS
--------------------------------------------------------------------------------

# Change file permissions
hdfs dfs -chmod 755 /user/koushik/data/file.csv

# Change permissions recursively
hdfs dfs -chmod -R 755 /user/koushik/data/

# Change owner
hdfs dfs -chown koushik:supergroup /user/koushik/data/file.csv

# Change group
hdfs dfs -chgrp supergroup /user/koushik/data/file.csv

--------------------------------------------------------------------------------
  REPLICATION
--------------------------------------------------------------------------------

# Change replication factor of a file
hdfs dfs -setrep -w 2 /user/koushik/data/file.csv

# Change replication factor recursively
hdfs dfs -setrep -w 2 -R /user/koushik/data/

================================================================================
