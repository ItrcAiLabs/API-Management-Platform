#!/bin/bash

# Script to configure MySQL databases for WSO2 API Manager

# Configuration variables (customize these as needed)
MYSQL_HOST="localhost"                  # MySQL server hostname
MYSQL_USER="root"                       # MySQL root user
MYSQL_PASSWORD="root_password"          # MySQL root password
API_M_HOME="/path/to/wso2am"            # Path to WSO2 API Manager directory

# Database names
SHARED_DB="shared_db"                   # Shared database for WSO2 components
APIM_DB="apim_db"                       # API Manager-specific database

# Database users and passwords
SHARED_USER="sharedadmin"               # Username for shared_db
SHARED_PASSWORD="sharedadmin"           # Password for shared_db user
APIM_USER="apimadmin"                   # Username for apim_db
APIM_PASSWORD="apimadmin"               # Password for apim_db user

# Function to run MySQL commands
execute_mysql() {
  mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "$1"
  if [ $? -ne 0 ]; then
    echo "Error: MySQL command failed: $1"
    exit 1
  fi
}

# Create databases with latin1 character set (required by WSO2)
execute_mysql "CREATE DATABASE IF NOT EXISTS $SHARED_DB character set latin1;"
execute_mysql "CREATE DATABASE IF NOT EXISTS $APIM_DB character set latin1;"

# Create users and grant privileges
execute_mysql "CREATE USER IF NOT EXISTS '$SHARED_USER'@'%' IDENTIFIED BY '$SHARED_PASSWORD';"
execute_mysql "GRANT ALL ON $SHARED_DB.* TO '$SHARED_USER'@'%';"
execute_mysql "CREATE USER IF NOT EXISTS '$APIM_USER'@'%' IDENTIFIED BY '$APIM_PASSWORD';"
execute_mysql "GRANT ALL ON $APIM_DB.* TO '$APIM_USER'@'%';"
execute_mysql "FLUSH PRIVILEGES;"

# Populate databases with WSO2 scripts
mysql -h "$MYSQL_HOST" -u "$SHARED_USER" -p"$SHARED_PASSWORD" "$SHARED_DB" < "$API_M_HOME/dbscripts/mysql.sql"
if [ $? -ne 0 ]; then
  echo "Error: Failed to execute mysql.sql for $SHARED_DB"
  exit 1
fi

mysql -h "$MYSQL_HOST" -u "$APIM_USER" -p"$APIM_PASSWORD" "$APIM_DB" < "$API_M_HOME/dbscripts/apimgt/mysql.sql"
if [ $? -ne 0 ]; then
  echo "Error: Failed to execute apimgt/mysql.sql for $APIM_DB"
  exit 1
fi

# Update deployment.toml configuration
DEPLOYMENT_TOML="$API_M_HOME/repository/conf/deployment.toml"

# Backup the original file
cp "$DEPLOYMENT_TOML" "$DEPLOYMENT_TOML.bak"
if [ $? -ne 0 ]; then
  echo "Error: Failed to backup deployment.toml"
  exit 1
fi

# Configure shared_db in deployment.toml
sed -i '/^\[database.shared_db\]/,/^\[/ {
  s|type = .*|type = "mysql"|
  s|url = .*|url = "jdbc:mysql://'$MYSQL_HOST':3306/'$SHARED_DB'?useSSL=false"|
  s|username = .*|username = "'$SHARED_USER'"|
  s|password = .*|password = "'$SHARED_PASSWORD'"|
}' "$DEPLOYMENT_TOML"

# Configure apim_db in deployment.toml
sed -i '/^\[database.apim_db\]/,/^\[/ {
  s|type = .*|type = "mysql"|
  s|url = .*|url = "jdbc:mysql://'$MYSQL_HOST':3306/'$APIM_DB'?useSSL=false"|
  s|username = .*|username = "'$APIM_USER'"|
  s|password = .*|password = "'$APIM_PASSWORD'"|
}' "$DEPLOYMENT_TOML"

echo "MySQL setup for WSO2 API Manager completed successfully!"