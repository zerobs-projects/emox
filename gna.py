#!/usr/bin/env python3
#
# gnar/runtime for EMOX-monitoring
#

version = "Release 5, v0.8.67, 2022-05-12"


import os
import sys
import time

import simplejson as json 

# https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7
from http.server import BaseHTTPRequestHandler, HTTPServer

import threading
from urllib.parse import urlparse
from config import *

try:
  iface = sys.argv[1]
except:
  iface = iface 
  


out_file = "stats"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

ok = "ok"
warn = "warn"
error = "error"

def get_bytes(t, iface):
  with open('/sys/class/net/' + iface + '/statistics/' + t + '_bytes', 'r') as f:
    data = f.read();
  return int(data)


def get_packets(t, iface):
  with open('/sys/class/net/' + iface + '/statistics/' + t + '_packets', 'r') as f:
    data = f.read();
  return int(data)

def out_write(stats):
  with open(out_file, "w") as f:
    f.write(json.dumps(stats))
  return()
  
def loggy(level, msg):
  dt= time.strftime("%H:%M", time.localtime(time.time()))
  if level == "warn":
    print("""%s[ %s ] [!!] %s %s""" % (bcolors.WARNING, dt, msg, bcolors.ENDC ))
    # ~ print(f"""{bcolors.WARNING}[ %s ] [!!] %s {bcolors.ENDC}""" % (dt, msg))
  elif level == "error":
    print("""%s[ %s ] [!!] %s %s""" % (bcolors.FAIL, dt, msg, bcolors.ENDC ))
  else:
    print("""%s[ %s ] %s %s""" % (bcolors.OKGREEN, dt, msg, bcolors.ENDC ))
    
  
  
class S(BaseHTTPRequestHandler):
  
  def _set_response(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.send_header('Server', 'Apache2.4')
    self.end_headers()

  def _set_auth(self):
    self.send_response(401)
    self.send_header('Content-type', 'go/fuckyourself')
    self.end_headers()


  def do_GET(self):
    # ~ loggy(ok, "GET request,\nPath: %s\nHeaders:\n%s\n" % (str(self.path), str(self.headers)))
    
    accepted_query = "idx=%s" % my_idx
    if self.path.find(accepted_query) > -1:
      with open(out_file, "rb") as o_f:
        c_stats = o_f.read() 
      self._set_response()
      self.wfile.write(c_stats)
      self.wfile.flush()      
      loggy(ok, c_stats)
    else:
      self._set_auth()
      return()

def welcome():

  print("""
  ___________   _____   ________  ____  ___      /\\      /\\  
\\_   _____/  /     \\  \\_____  \\ \\   \\/  /     / /     / /
 |    __)_  /  \\ /  \\  /   |   \\ \\     /     / /     / / 
 |        \\/    Y    \\/    |    \\/     \\    / /     / /  
/_______  /\\____|__  /\\_______  /___/\\  \\  / /     / /     
        \\/         \\/         \\/      \\_/  \\/      \\/        
          v %s 
         (c) copyright 2020-2022 zeroBS GmbH
""" % version)


def run_server(server_class=HTTPServer, handler_class=S, port=srv_port):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  loggy(ok, 'Starting httpd on port: %s ...\n' % srv_port)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  httpd.server_close()
  loggy(ok, 'Stopping httpd...\n')
  

stats = {

    "rx": { "bytes": 0, "packets": 0, "avg": 0},
    "tx": { "bytes": 0, "packets": 0, "avg": 0},
    

}

welcome()

# lets start the webserver
x = threading.Thread(target=run_server, args=())
# ~ loggy(ok, "Main    : before running thread")
x.start()

loggy(ok, "[i] collecting stats for iface [ %s ] " % iface)



while 1:
  rx1 = get_bytes("rx", iface)
  tx1 = get_bytes("tx", iface)
  rp1 = get_packets("rx", iface)
  tp1 = get_packets("tx", iface)

  # ~ loggy(ok, "[i] collecting stats for iface [ %s ] " % iface)
  try:
    time.sleep(5)
  except:
    loggy(warn, "exiting, interrupt")
    sys.exit()
    x.stop()

  rx2 = get_bytes("rx", iface)
  tx2 = get_bytes("tx", iface)
  rp2 = get_packets("rx", iface)
  tp2 = get_packets("tx", iface)
  
  rx = rx2 - rx1
  tx = tx2 - tx1
  rp = rp2 - rp1
  tp = tp2 - tp1
  
  stats["rx"]["bytes"] = int(rx * 8 / 5)
  stats["rx"]["packets"] = int(rp / 5)
  stats["tx"]["bytes"] = int(tx * 8 / 5)
  stats["tx"]["packets"] = int(tp / 5)
  try:
    stats["rx"]["avg"] = int(rx / rp)
  except:
    stats["rx"]["avg"] = 0

  try:
    stats["tx"]["avg"] = int(tx / tp)
  except:
    stats["tx"]["avg"] = 0
    
  out_write(stats)
  loggy(ok, stats)
  
  
  
  
  

  
