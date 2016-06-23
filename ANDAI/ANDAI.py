build = "6.13.2016"
version = "1.0.2"
print "Starting Minecraft Launcher v%s Alpha, build %s" % (version, build)
import getpass
import logging
import os
import random
import shutil
import socket
import subprocess
import sys
import time
import tkMessageBox
import ttk
import urllib
import urllib2
from Tkinter import *

try:
    import DownloadANDAI
except:
    print "[%s ERR]: The module 'DownloadANDAI' could not be imported. Downloading... %d" % time.strftime("%H:%M:%S"), 5
    os.mkdir("%s-%d" % "test", 5)
    urllib.urlretrieve("https://raw.githubusercontent.com/Unknown025/A-Nation-Divided-Against-Itself-Launcher/master/DownloadANDAI.py", "DownloadANDAI.py")
    import DownloadANDAI
    None = True
try:
    import requests
except ImportError as e:
    print "[%s ERR]: The module 'requests' could not be imported. The process cannot continue." % (
    time.strftime("%H:%M:%S"))
    sys.exit(1)

try:
    computer_name = os.environ['COMPUTERNAME']
except KeyError:
    computer_name = socket.gethostname()
user = getpass.getuser()
LOG_FILENAME = "launcher.log"
FORMAT = '[%(asctime)s %(levelname)s]: %(message)s'
logging.basicConfig(filename=LOG_FILENAME, format=FORMAT, level=0)
print "[%s INFO]: Finished loading." % (time.strftime("%H:%M:%S"))
logging.info("Username is: %s" % user)
if not os.path.exists(".minecraft"):
    try:
        os.mkdir(".minecraft")
        logging.info("Created .minecraft")
    except OSError as e:
        print "[%s INFO]: .minecraft already exists." % (time.strftime("%H:%M:%S"))
else:
    print "[%s INFO]: Found the .minecraft folder." % (time.strftime("%H:%M:%S"))
os.chdir(".minecraft")
Failed = 0
Succeeded = 0
clientToken = random.randint(1000, 9999)
import json

x = 0
try:
    root = Tk()
except:
    logging.critical("A critical error has occured and Tkinter cannot be initiated.")
    sys.exit(0)
root.title("Minecraft Launcher (v%s)" % (version))
try:
    root.iconbitmap("custom_icon.ico")
except TclError as e:
    urllib.urlretrieve(
        "https://raw.githubusercontent.com/Unknown025/A-Nation-Divided-Against-Itself-Launcher/master/custom_icon.ico",
        "custom_icon.ico")
    logging.info(
        "Downloaded custom_icon.ico from https://raw.githubusercontent.com/Unknown025/A-Nation-Divided-Against-Itself-Launcher/master/custom_icon.ico")
    root.iconbitmap("custom_icon.ico")
Frame = ttk.LabelFrame(root, text="Minecraft Launcher")
Frame.pack()


def makeDir(dirname):
    if currentOS == "linux":
        os.system("mkdir -p " + dirname)
    else:
        # Windows
        # os.system("MD " + dirname.replace("/", "\\") + " 2>NUL")
        subprocess.call("MD " + dirname.replace("/", "\\") + " 2>NUL", shell=True)


currentOS = None
if sys.platform.startswith("win"):
    currentOS = "windows"
    logging.info("Current OS: Windows")
else:
    currentOS = "linux"

bits = "32"
if sys.maxint == 9223372036854775807:
    bits = "64"


def internet_on():
    try:
        response = urllib2.urlopen('http://74.125.228.100', timeout=1)
        return True
    except urllib2.URLError as err:
        pass
    return False


FailedFiles = 0
DownloadedFiles = 0

def launchMC():
    tkMessageBox.showinfo("Warning!",
                          "This launcher is not fully functional yet. For safety purposes, Forge functionality has been disabled. Also, the launcher will appear to freeze when downloading files. Please be patient.")
    p = DownloadANDAI.Profile("1.7.10")
    p.downloadMissingFiles()
    # p.downloadForge()
    if os.path.isfile("usernamecache.json"):
        shutil.copyfile("usernamecache.json", "mcdata\\usernamecache.json")
    else:
        print "[%s ERR]: User not authenticated/usernamecache.json not found." % (time.strftime("%H:%M:%S"))
        win = open("usernamecache.json", "w")
        win.write("Player\nnull\nnull")
    os.chdir("mcdata")
    # command="cd mcdata && %s" % (p.launchcmd(username))
    creds.withdraw()
    if FailedFiles > 0:
        print "[WARN]: Attempting to launch, likely without the right files."
        try:
            subprocess.Popen(p.launchcmd(), shell=True)
        except:
            tkMessageBox.showerror("Error!",
                                   "An error has cccured, and Minecraft cannot be launched.\n%s files could not be downloaded. (Error #E12)" % FailedFiles)
        tkMessageBox.showerror("Error!",
                               "An error has cccured, and Minecraft cannot be launched.\n%s files could not be downloaded. (Error #D34)" % FailedFiles)
    else:
        pass
        subprocess.Popen(p.launchcmd(), shell=False)


creds = Toplevel()
creds.minsize(width=400, height=100)
UsrFrame = ttk.LabelFrame(creds, text="Username")
username = ttk.Entry(UsrFrame)
UsrFrame.pack()
username.pack()
PassFrame = ttk.LabelFrame(creds, text="Password")
password = ttk.Entry(PassFrame, show='*')
PassFrame.pack()
password.pack()


def onclose():
    creds.grab_release()
    creds.withdraw()


creds.protocol('WM_DELETE_WINDOW', onclose)


def validate():
    invalid = """{u'errorMessage': u'Invalid credentials.', u'error': u'ForbiddenOperationException'}"""
    data = json.dumps(
        {"agent": {"name": "Minecraft", "version": 1}, "username": username.get(), "password": password.get(),
         "clientToken": ""})
    headers = {'Content-Type': 'application/json'}
    r = requests.post('https://authserver.mojang.com/authenticate', data=data, headers=headers)
    output = r.json()
    logging.info(output)
    print output
    try:
        file_output = "%s\n%s\n%s" % (
        str(output["selectedProfile"]["name"]), str(output["selectedProfile"]["id"]), str(output["accessToken"]))
        win = open("usernamecache.json", "w")
        win.write(file_output)
        win.close()
    except:
        tkMessageBox.showerror(title="Credentials Invalid.",
                               message="It appears to be that your credentials are not valid. Please try again.")
    else:
        onclose()
        launchMC()


def showlogin():
    creds.deiconify()
    creds.grab_set()


chk = ttk.Button(creds, text="Login", command=validate)
chk.pack()


def serverping():
    import struct

    def unpack_varint(s):
        d = 0
        for i in range(5):
            b = ord(s.recv(1))
            d |= (b & 0x7F) << 7 * i
            if not b & 0x80:
                break
        return d

    def pack_varint(d):
        o = ""
        while True:
            b = d & 0x7F
            d >>= 7
            o += struct.pack("B", b | (0x80 if d > 0 else 0))
            if d == 0:
                break
        return o

    def pack_data(d):
        return pack_varint(len(d)) + d

    def pack_port(i):
        return struct.pack('>H', i)

    def get_info(host='73.254.106.2', port=40001):

        # Connect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        # Send handshake + status request
        s.send(pack_data("\x00\x00" + pack_data(host.encode('utf8')) + pack_port(port) + "\x01"))
        s.send(pack_data("\x00"))

        # Read response
        unpack_varint(s)  # Packet length
        unpack_varint(s)  # Packet ID
        l = unpack_varint(s)  # String length

        d = ""
        while len(d) < l:
            d += s.recv(1024)

        # Close our socket
        s.close()

        # Load json and return
        return json.loads(d.decode('utf8'))

    return get_info()


creds.withdraw()


def credentials():
    if validate() == False:
        creds.deiconify()
        creds.grab_set()
    else:
        validate()


def ask_validate():
    if tkMessageBox.askyesno("Validation", "Would you like to authenticate with Mojang before continuing?"):
        showlogin()
    else:
        launchMC()


Frame = ttk.LabelFrame(root, text="Server Status")
Frame.pack()
var = StringVar()
ServerStatus = ttk.Label(Frame, textvariable=var)
data = serverping()
output = "Server: %s\nOnline: %s" % (data["description"], data["players"]["online"])
var.set(output)
ServerStatus.pack()
Launch = ttk.Button(root, text="Launch", command=ask_validate)
Launch.pack()
root.minsize(width=500, height=250)
info = "You are running ANDAI Launcher.\nCurrent version: v%s\nCurrent build: %s" % (version, build)
tkMessageBox.showinfo(None, info)
root.mainloop()
sys.exit(0)
