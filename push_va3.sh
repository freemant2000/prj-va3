#!/bin/bash
mysqldump -u kenttong -h kenttong.mysql.pythonanywhere-services.com -p kenttong\$va3 --set-gtid-purged=OFF --no-tablespaces > va3.dump
git commit -a -m "update"
git push
