HP 3D DriveGuide Daemon for HP notebooks
==============

Tech Intro:
--------------

[See this HP PDF](http://www.hp.com/sbso/solutions/pc_expertise/professional_innovations/hp-3d-drive-guard.pdf)

Usage: 
--------------

Copy:

- driveguardd.py to /usr/local/bin/driveguardd 
- conf/driveguardd.conf to /etc
- init.d/driveguardd to /etc/init.d

Logging goes to syslog. Syntax is compatible with python3 and its the default

And for Ubuntu/Debian users, update-rc.d driveguardd defaults

ToDo:
--------------

1. Implement closed-lid parking.
2. Use python easy setup to make things.
3. Increase code legibility.

Thanks:
--------------

A lot of things i did may not happen w/o Ricardo Canale <ricardo.canale@usp.br> and his mother concerning Notebook Donation ;)

