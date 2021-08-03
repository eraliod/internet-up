FROM python:3.9.0b4-alpine3.12
COPY /scripts/internetUp.py /bin/internetUp.py
COPY root /var/spool/cron/crontabs/root
RUN chmod +x /bin/internetUp.py
RUN pip install requests datetime
# ***** Had to add tzdata package to get TZ variable to work in alpine
RUN apk add -U tzdata 
CMD crond -l 2 -f