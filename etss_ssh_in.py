#!/usr/bin/env python
#
# Copyright (c)  2013 Hewlett-Packard Development Company, L.P.
#
# Permission is hereby granted, fpenrlowee of charge, to any person
# obtaining a copy of this software  and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#
# This script provides possibility to run range ping from the switch.
# It will access IP or range of IP addresses as parameter.
# Ranges can be specified in the following formats,
# python etss_ping.py 192.168.56.0/24 than use 192.168.56-57.0-255

import paramiko
import sys
import os
import time

test = os.system('ping 192.168.56.102')

cmd = "display version\n"
host = '192.168.56.102'
user = 'dobias'
passwd = 'HPRocks2'

ip = sys.argv[1]


def screen_disable(remote):
    #Turn of pausing between screens of output

    remote.send('screen-length disable\n')
    time.sleep(1)

    #Clear the on screen buffer
    output = remote.recv(1000)

    return output

def etss_range(etssrange):
    hosts = []
    block = etssrange.split('.')
    for x, y in enumerate(block):
        if '-' in y:
            blockrange = y.split('-')
            for z in range(int(blockrange[0]), int(blockrange[1])+1):
                ipaddr = '.'.join(block[:x] + [str(z)] + block[x+1:])
                hosts += etss_range(ipaddr)
            break
    else:
        hosts.append(etssrange)
    return hosts



def main():
    target_ip = etss_range(ip)
    print target_ip
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for i in target_ip:
        try:
            ssh.connect(i, username=user, password=passwd)
            print "SSH connection established to %s" % (i)
            remote = ssh.invoke_shell()
            print "Interactive SSH session established"
            output = remote.recv(1000)
            print output
            #Disable pausing between screens of output
            screen_disable(remote)
            #Send commands to network device
            remote.send('\n')
            remote.send(cmd)
            time.sleep(2)
            output = remote.recv(5000)
            print output
        except:
            ssh.close()
            print "Problem connecting with ip: %s" % (i)
            continue

if __name__ == "__main__":
    main()

