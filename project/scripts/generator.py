from csv import writer
from datetime import datetime, timedelta
from os import path

if not path.exists('log.csv'):
    with open('log.csv','w') as log_file:
        log_writer = writer(log_file)
        log_header = ['timestamp','connection','provider','status_code','public_ip']
        log_writer.writerow(log_header)


with open('log.csv','a') as log_file:
    log_writer = writer(log_file)

    x = 0
    now_start = datetime.now()

    while x < 50000:
        x+=1
        now = now_start + timedelta(minutes=x)
        log = [now.strftime("%Y-%m-%d %H:%M")]
        log.extend(['connected','google',200,'69.14.125.32'])
        log_writer.writerow(log)

    while x < 80000:
        x+=1
        now = now_start + timedelta(minutes=x)
        log = [now.strftime("%Y-%m-%d %H:%M")]
        log.extend(['connected','google',200,'69.14.132.120'])
        log_writer.writerow(log)
    
    while x < 100000:
        x+=1
        now = now_start + timedelta(minutes=x)
        log = [now.strftime("%Y-%m-%d %H:%M")]
        log.extend(['connected','google',200,'69.33.43.235'])
        log_writer.writerow(log)

    while x < 120000:
        x+=1
        now = now_start + timedelta(minutes=x)
        log = [now.strftime("%Y-%m-%d %H:%M")]
        log.extend(['connected','google',200,'69.33.34.176'])
        log_writer.writerow(log)

    while x < 150000:
        x+=1
        now = now_start + timedelta(minutes=x)
        log = [now.strftime("%Y-%m-%d %H:%M")]
        log.extend(['connected','google',200,'69.33.45.24'])
        log_writer.writerow(log)
    print(x)