#!/bin/bash

echo "

[i] starting EMOX-Installation for zeroBS

"

apt -y update
# not on client-systems
#apt -y upgrade 

apt -y install python3-simplejson tmux

echo '

iface = "eth0"
srv_port = 6040

my_idx = "icanhazcheesburgerZ1337"


' > config.py
echo "

> sample_config created

"


my_dir=`pwd`

# runnign cronjob_adding now
(crontab -l | echo "@reboot cd $my_dir && ./run.sh" | crontab -)

echo "

> cronjob added

"

echo "


EMOX-Installation done, feel free
to adjust 

config.py

"

