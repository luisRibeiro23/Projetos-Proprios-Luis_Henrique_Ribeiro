tail -f /var/log/syslog | while read LINE
do
    echo "$LINE"
done
