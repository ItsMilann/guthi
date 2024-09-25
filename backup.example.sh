#!/bin/bash

DATE=`date +%Y%m%d`
PROJECT_NAME="patrachar"
CONTAINER_NAME="patrachar_postgres"
USER="patrachar"
DB_NAME="patrachar"
BACKUP_DIR="/home/ideabreed/backup/$PROJECT_NAME/"
BACKUP_FILE="$BACKUP_DIR/$DATE.sql" 
SERVER_DIR="/home/ideabreed/backups/siyari/$PROJECT_NAME"
# remote server where backup file is to be upload | format: user@ip_address
BACKUPSERVER="root@139.59.86.208"

mkdir -p $BACKUP_DIR
docker exec -t $CONTAINER_NAME pg_dumpall -c -U $USER > $BACKUP_FILE

if [[ "$BACKUPSERVER" ]]; then 
	ssh $BACKUPSERVER "mkdir -p $SERVER_DIR";
	scp -p $BACKUP_FILE $BACKUPSERVER:$SERVER_DIR
fi

# paste the following line
# (crontab -l 2> /dev/null; echo "0 * * * * /bin/bash $PWD/backup.sh >> /home/ideabreed/crontab.log 2>&1") | crontab -
