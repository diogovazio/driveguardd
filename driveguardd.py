#!/usr/bin/env python3

# This file is part of driveguardd. Driveguardd is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Leonardo Amaral <contato@leonardoamaral.com.br>
#
# Inspired in http://lkml.indiana.edu/hypermail/linux/kernel/0811.3/01905.html
#
# Thanks To: Ricardo Canale <ricardo.canale@usp.br> 
#            And his mother for the Notebook Donation ;)
#

from configparser import ConfigParser as configparser
from time import sleep
from syslog import syslog,openlog,LOG_DAEMON,LOG_INFO,LOG_WARNING,LOG_NOTICE
from os import getpid
import struct,signal,sys

opts = configparser()
opts.read('/etc/driveguardd.conf')

PID=getpid()

openlog('Driveguardd [%d]' % PID, 0, LOG_DAEMON)

with open('/var/run/driveguardd.pid','w') as pidfile:
	pidfile.write(str(PID)+'\n')

def exit_handler(signalsent, frame):
    if signalsent == signal.SIGTERM or signalsent == signal.SIGINT:
        syslog(LOG_NOTICE, 'Stopping daemon.')
        sys.exit(0)
    else:
        syslog(LOG_WARNING, 'Unexpected signal received. Keeping alive')
    return(-1)

def getopt(section):
    dict1 = {}
    options = opts.options(section)
    for option in options:
        try:
            dict1[option] = opts.get(section, option)
        except:
            syslog(LOG_WARNING, "getopt: exception on %s!" % option)
            dict1[option] = None
    return dict1

def fallaction(interrupts, time):

    '''Fall action parks the disk in case of fall. Interrupts is the parameter to
       see how many fall /dev/freefall got - not used for now and time is how much
       disk will stay parked.
    '''
    with open('/sys/block/sda/device/unload_heads','w') as hdd_heads:
    	hdd_heads.write(str(time)+'\n')
    with open('/sys/class/leds/hp::hddprotect/brightness','w') as hp3dg_led:
    	hp3dg_led.write('1')
    syslog(LOG_WARNING, 'Computer Falling! PARKING disk.')
    
    while True:
        with open('/sys/block/sda/device/unload_heads','r') as hdd_heads:
            with open('/sys/class/leds/hp::hddprotect/brightness','w') as hp3dg_led:
                sleep(100.0/1000.0)
                if int(hdd_heads.read()) == 0:
                    hp3dg_led.write('0')
                    syslog(LOG_NOTICE, 'Disk comes back.')
                    break
    return 0

def mainLoop():
    syslog(LOG_NOTICE, 'HP 3D Drive Guard Daemon Started.')
    syslog(LOG_NOTICE, 'Device: %s' % getopt('Readaccel')['device'])
    with open('/sys/class/leds/hp::hddprotect/brightness','w') as hp3dg_led:
        hp3dg_led.write('0')

    while True:
        with open(getopt('Readaccel')['device'],'rb') as freefall:
            interrupt = int(struct.unpack('B',freefall.read(1))[0])
        fallaction(interrupt, 10100)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)
    mainLoop()
