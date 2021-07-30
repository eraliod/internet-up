#!/usr/bin/python
import requests
from csv import writer
from datetime import datetime
from os import path


def checkInternet():
    '''creates a log entry that contains details on a simple internet health check. It also lists the public ip address assigned by the ISP'''
    
    #ensure the log.csv file exits, if not then create it with the header row
    if not path.exists('../data/log.csv'):
        with open('../data/log.csv', mode='w', newline='') as log_file:
            log_writer = writer(log_file)
            log_header = ['timestamp','connection','provider','status_code','public_ip']
            log_writer.writerow(log_header)

    #set variables to None so they will exist even if all try blocks fail
    google = None
    aws = None

    #check the time and begin the list of items for each row in the log
    now = datetime.now()
    log = [now.strftime("%Y-%m-%d %H:%M")]

    #attempt a simple GET request to google.com, looking for a response
    try:
        google = requests.get('https://google.com', timeout=5).status_code
        if google == 200:
            log.extend(['connected','google',str(google)])
        pass
    except requests.exceptions.RequestException as e:
        pass
    
    #attempt a simple GET request to aws.com, looking for a response - ONLY IF google failed
    if google != 200:
        try:
            aws = requests.get('https://aws.com', timeout=5).status_code
            if aws == 200:
                log.extend(['connected','aws',str(aws)])
            pass
        except requests.exceptions.Timeout:
            log.extend(['error','aws','timeout'])
        except requests.exceptions.ConnectionError:
            log.extend(['error','aws','unreachable'])
        except requests.exceptions.RequestException as e:
            log.extend(['error','aws',e])
    pass

    #if either google or aws checks succeed, retrieve the host public ip address
    if google == 200 or aws == 200:
        try:
            ip = requests.get('https://api.ipify.org').text
            ip_split = ip.split('.')
            #Quick check to ensure the ipify API text is returning a valid IP address format
            ip_error_count = 0
            for bit in ip_split:
                if len(bit) <= 3:
                    pass
                else:
                    ip_error_count+=1
            if ip_error_count == 0:
                log.append(ip)
            else:
                raise Exception('text returned from ipify is not an ip')
        except requests.exceptions.RequestException as e:
            log.append('ip error')
    else:
        log.append('None')

    #Append the log row out to the log.csv file
    with open('../data/log.csv', mode='a', newline='') as log_file:
        log_writer = writer(log_file)
        log_writer.writerow(log)

    return(print(log))

checkInternet()