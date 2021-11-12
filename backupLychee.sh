rsync -av --progress --log-file=/home/bret/photoserver/logs/rsync.log \
  root@hessminecraft.cyou:/home/photoserver/Lychee \
   /media/sf_backup/photoserverLychee/rsyncLychee
python3 /home/bret/photoserver/summaryEmailLogs.py
mv -f /home/bret/photoserver/logs/rsync.log /home/bret/photoserver/logs/copyrsync.log