import urllib
import urllib.request # had to add for python 3.4 -jc
import socks
import socket
#import socket
import argparse
import random
import sys


import pymysql

import pymysql as my

# Open database connection
conn = my.connect(host='127.0.0.1', user='user', passwd='pass', db='myproject', charset='utf8', init_command='SET NAMES UTF8')

parser = argparse.ArgumentParser()
parser.add_argument('-o', action='store', dest='onion',
                    help='put in onion site to load (with http & quotes)') # set -o to accept onion address
results = parser.parse_args()


roham = input (" Enter Your URL Onion : >>> ")
onionsite = roham
if results.onion != None:
	onionsite = results.onion
print("we Are Connection to The Tor Network ... ")

SOCKS_PORT = 9050

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1",SOCKS_PORT)
socket.socket = socks.socksocket


def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
socket.getaddrinfo = getaddrinfo


headers = {'User-Agent': '' }

req = urllib.request.Request(onionsite,None,headers)
response = urllib.request.urlopen(req) # new python 3 code -jc
status = 'loaded successfully'
try:
	sitehtml = response.read()
	print (sitehtml)

except urllib.error.URLError as e:

    html = e.read().decode("utf8", 'ignore')
    status = 'failed reading'
    html = 'none'
    currenturl = 'none'
    print (status)
    exit()




c = conn.cursor()
c.execute("SELECT * FROM GetUrl_url_info")
c.execute("""
INSERT INTO GetUrl_url_info (url_title,url_body,url_add) VALUES (%s,%s,%s) """,(onionsite,sitehtml, onionsite))
conn.commit()
print('Succesfully Inserted the values to DB !')
