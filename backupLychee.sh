rsync -av --progress --log-file=/home/bret/photoserver/logs/rsync.log \
  root@hessminecraft.cyou:/home/photoserver/Lychee \
   /media/sf_photoserverLychee/rsyncLychee 
python3 summaryEmailLogs.py