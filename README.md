# Pi-Status-over-HTTP
Single python script to output raspberry pi status over http. The python script acts as both the http server and status page.

Memory consumption of about 4 MB while running the HTTP server.

Just place the file in your /home/pi/ directory open it in any note editor and add it to boot by following the instructions at the top of the python file.


Extract from the file:

```
# To start at boot, you can either setup a cron tab as following:
# Edit crontabs by running the command: 
#     crontab -e
# And add to file:
#     @reboot python3 /home/pi/status.py &
#
# Or set it up in /etc/rc.local [before] the "exit 0" line as following:
# Edit rc.local file by running the command: 
#     sudo nano /etc/rc.local
# And add to file:
#     python3 /home/pi/status.py &
#
# Do note that you do not need to run it as sudo
#
```
