tmp=`ps -ef|grep uwsgi |grep -v grep|awk '{print $2}'` 
echo ${tmp} 
kill -9 ${tmp} 
`uwsgi /home/mysite/script/uwsgi.ini -d /home/mysite/script/log/uwsgi.log`
`service nginx reload`