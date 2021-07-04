#!/usr/bin/env python3

# --- README ---
#
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



from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import subprocess


hostName = "" # Any hostname
serverPort = 7828 # Port for "STAT" status server

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        
        # Shell scripts for system monitoring from here:
        # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
        IP = "IP: " + IP.strip() #IP comes with free \n so we remove it
        self.wfile.write(bytes(IP+"\n", "utf-8")) 
        
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
        self.wfile.write(bytes(CPU+"\n", "utf-8"))
        
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
        self.wfile.write(bytes(MemUsage+"\n", "utf-8"))
        
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%d GB  %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
        self.wfile.write(bytes(Disk+"\n", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    IP = "IP: " + IP.strip()
    print("Server started http://%s:%s" % (IP, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")



