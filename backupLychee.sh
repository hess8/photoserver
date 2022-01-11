rsync -av --progress --log-file=/home/bret/photoserver/logs/rsync.log \
  root@hessminecraft.cyou:/home/photoserver/Lychee \
   /media/sf_backup/photoserverLychee/rsyncLychee
python3 /home/bret/photoserver/summaryEmailLogs.py
mv -f /home/bret/photoserver/logs/rsync.log /home/bret/photoserver/logs/copyrsync.log
## make a database file copy
_now=$(date +"%Y_%m_%d")
_databasefile="/media/sf_backup/photoserverLychee/rsyncLychee/Lychee/database/database.sqlite"
_backupfile="/media/sf_backup/photoserverLychee/databaseDailyCopy/database_$_now.sqlite"
cp "$_databasefile" "$_backupfile"