#!/bin/bash
#
# v0.2 2022-07-20


echo "

[i] starting nginx for  EMOX-Installation

"

my_dir=`pwd`


apt -y update
# not on client-systems
#apt -y upgrade 

apt -y install nginx openssl

echo "

> creating fake ssl-certs for nginx

"

mkdir -p /etc/nginx/ssl

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt

my_random=`echo $RANDOM | md5sum | head -c 20; echo;`

# create now a nginx-configfile
echo "

server {
        listen 4443 ssl;
        #listen [::]:443 ssl;


        root /var/www/html;


        ssl_certificate /etc/nginx/ssl/nginx.crt;
        ssl_certificate_key /etc/nginx/ssl/nginx.key;

        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location /$my_random {
          
          alias $my_dir;
        
      }

}
" > /etc/nginx/sites-enabled/gna-ssl


service nginx restart


echo "

your path to to access the stats-file:

https://THIS_IP/$my_random/stats


"

