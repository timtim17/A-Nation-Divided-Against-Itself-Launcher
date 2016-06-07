version="1.0.0"
print "Starting Minecraft Launcher v%s" % (version)
from Tkinter import *
import ttk
import tkMessageBox
import urllib, urllib2
import time
import subprocess
import shutil
import ntpath
import os
import sys
import random
from multiprocessing import Process
import threading
print "[%s INFO]: Finished loading." % (time.strftime("%H:%M:%S"))
try:
    import requests
except ImportError as e:
    print "[%s ERR]: The module 'requests' could not be imported. The process cannot continue." % (time.strftime("%H:%M:%S"))
    sys.exit(1)
from zipfile import ZipFile, BadZipfile
if os.path.exists(".minecraft")==False or os.path.exists("launcher")==False:
    try:
        os.mkdir(".minecraft")
    except WindowsError as e:
        print "[%s INFO]: .minecraft already exists." % (time.strftime("%H:%M:%S"))
else:
    print "[%s INFO]: Found the .minecraft folder." % (time.strftime("%H:%M:%S"))
os.chdir(".minecraft")
Failed=0
Succeeded=0
clientToken=random.randint(1000, 9999)
import json
x=0
root=Tk()
root.title("Minecraft Launcher (v%s)" % (version))
root.iconbitmap("C:\Users\Sasha\Downloads\custom_icon.ico")
Frame=ttk.LabelFrame(root, text="Minecraft Launcher")
Frame.pack()

def makeDir(dirname):
    if currentOS == "linux":
        os.system("mkdir -p " + dirname)
    else:
        # Windows
        #os.system("MD " + dirname.replace("/", "\\") + " 2>NUL")
        subprocess.call("MD " + dirname.replace("/", "\\") + " 2>NUL", shell=True)
currentOS = None
if sys.platform.startswith("win"):
    currentOS = "windows"
else:
    currentOS = "linux"

bits = "32"
if sys.maxint == 9223372036854775807:
    bits = "64"
def internet_on():
    try:
        response=urllib2.urlopen('http://74.125.228.100',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False




class Profile:
    def __init__(self, version):
                #tk.Tk.__init__(self)
                #self.download=Toplevel(root)
                #self.download.grab_set()
                #self.progress=ttk.Progressbar(download, orient=horizontal, length=200, mode='determinate')
                #self.progress.pack()
        self.version = version
        self.libs = []
        self.fileIndex = [("mcdata/versions/%s/%s.json" % (self.version, self.version),
                    "http://s3.amazonaws.com/Minecraft.Download/versions/%s/%s.json" % (self.version, self.version)),

                    ("mcdata/versions/%s/%s.jar" % (self.version, self.version),
                    "http://s3.amazonaws.com/Minecraft.Download/versions/%s/%s.jar" % (self.version, self.version))
        ]

        # Load version info
        f = None
        try:
            f = open("mcdata/versions/%s/%s.json" % (self.version, self.version), "rb")
        except IOError:
            makeDir("mcdata/versions/%s" % self.version)
            self.cdownload1=threading.Thread(target=self.downloadFile, args=("mcdata/versions/%s/%s.json" % (self.version, self.version),
                    "http://s3.amazonaws.com/Minecraft.Download/versions/%s/%s.json" % (self.version, self.version))
            )
            self.cdownload1.start()
            self.cdownload1.join()
            f = open("mcdata/versions/%s/%s.json" % (self.version, self.version), "rb")
        sdata = f.read()
        f.close()

        self.versionInfo = json.loads(sdata)
        self.mainClass = self.versionInfo["mainClass"]
        self.mcargs = self.versionInfo["minecraftArguments"]
        self.jar = "versions/%s/%s.jar" % (self.version, self.version)
        for libinfo in self.versionInfo["libraries"]:
            librep = libinfo.get("url", "https://libraries.minecraft.net/")
            name = libinfo["name"]
            package, name, version = name.split(":")
            relpath = package.replace(".", "/") + "/" + name + "/" + version + "/" + name + "-" + version + ".jar"
            self.fileIndex.append(("mcdata/libraries/" + relpath, librep + relpath))
            self.libs.append("libraries/" + relpath)

            if libinfo.has_key("natives"):
                if libinfo["natives"].has_key(currentOS):
                    makeDir("mcdata/natives")
                    natstr = libinfo["natives"][currentOS].replace("${arch}", bits)
                    relpath = package.replace(".", "/") + "/" + name + "/" + version + "/" + name + "-" + version + "-" + natstr + ".jar"
                    libpath = "mcdata/libraries/" + relpath
                    liburl = librep + relpath
                    if not os.path.exists(libpath):
                        self.cdownload2=threading.Thread(target=self.downloadFile, args=(libpath, liburl))
                        self.cdownload2.start()
                        self.cdownload2.join()
                        print ">Extract " + libpath
                        try:
                            zipfile = ZipFile(libpath, "r")
                            for name in zipfile.namelist():
                                if not (name.startswith("META-INF") or name.startswith(".")):
                                    zipfile.extract(name, "mcdata/natives")
                            zipfile.close()
                        except BadZipfile:
                            print "[%s WARN]: A faulty zip or jar file was found. This may cause problems!" % (time.strftime("%H:%M:%S"))
                            try:
                                os.remove(libpath)
                            except:
                                pass

        # We must also get the assets index.
        assetsName = self.versionInfo.get("assets", "legacy")
        assetsIndexFile = "mcdata/assets/indexes/%s.json" % assetsName
        assetsIndexLink = "https://s3.amazonaws.com/Minecraft.Download/indexes/%s.json" % assetsName
        self.cdownload3=threading.Thread(target=self.downloadFile, args=(assetsIndexFile, assetsIndexLink))
        self.cdownload3.start()
        self.cdownload3.join()
        assetsIndexFile=str(assetsIndexFile)
        f = open(assetsIndexFile, "rb")
        assetsData = json.loads(f.read())
        f.close()

        for key, value in assetsData["objects"].items():
            hash = value["hash"]
            pref = hash[:2]
            self.fileIndex.append((
                "mcdata/assets/objects/%s/%s" % (pref, hash),
                "http://resources.download.minecraft.net/%s/%s" % (pref, hash)
            ))
    def downloadFile(self, filename, url):
        print "[%s INFO]: Downloading: %s" % (time.strftime("%H:%M:%S"), filename)
        dirname = filename.rsplit("/", 1)[0]
        makeDir(dirname)
        inf = urllib.urlopen(url)
        outf = open(filename, "wb")
        while 1:
            b = inf.read(1)
            if len(b) == 0:
                break
            else:
                outf.write(b)
        inf.close()
        outf.close()
        print "[%s INFO]: Finished downloading: %s" % (time.strftime("%H:%M:%S"), filename)
        sys.exit(0)

    def downloadMissingFiles(self):
        print "[%s INFO]: Started downloading missing fies." % (time.strftime("%H:%M:%S"))
        running_downloads = []
        for filename, url in self.fileIndex:
            if not os.path.exists(filename):
                if len(running_downloads) > 20:
                    for f in running_downloads:
                        f.join()
                    running_downloads=[]
                downloadmfiles=threading.Thread(target=self.downloadFile, args=(filename, url))
                downloadmfiles.start()
                running_downloads.append(downloadmfiles)
                root.after(500)
                #self.downloadmfiles.join()
        for f in running_downloads:
            f.join()

    def launchcmd(self, username = "MinecraftPlayer"):
        libs = [self.jar]
        libs.extend(self.libs)
        cp = ":".join(libs)
        if currentOS == "windows":
            # LOL
            cp = ";".join(libs).replace("/", "\\")
        try:
            self.win=open("usernamecache.json", "r")
            self.username=self.win.readline()
            self.auth_uuid=self.win.readline()
            self.auth_access_token=self.win.readline()
            self.username=self.username.rstrip()
            self.auth_uuid=self.auth_uuid.rstrip()
            self.auth_access_token=self.auth_access_token.rstrip()
            print self.username
            print self.auth_uuid
            print self.auth_access_token
        except:
            print "[WARN]: Authentication failed!"
            self.username="null"
            self.auth_uuid="null"
            self.auth_access_token="null"
        args = self.mcargs
        args = args.replace("${auth_player_name}", self.username)
        args = args.replace("${version_name}", self.version)
        args = args.replace("${game_directory}", ".")
        args = args.replace("${game_assets}", "assets")		# Not even used.
        args = args.replace("${assets_root}", "assets")		# Not even used.
        args = args.replace("${auth_uuid}", self.auth_uuid)
        args = args.replace("${auth_access_token}", self.auth_access_token)
        args = args.replace("${assets_index_name}", self.versionInfo.get("assets", "legacy"))
        args = args.replace("${user_properties}", "{}")
        args = args.replace("${user_type}", "online")
        return 'java -cp "%s" -Djava.library.path=natives %s %s' % (cp, self.mainClass, args)


def launchMC():
    p=Profile("1.7.10")
    p.downloadMissingFiles()
    shutil.copyfile("usernamecache.json", "mcdata\\usernamecache.json")
    os.chdir("mcdata")
    #command="cd mcdata && %s" % (p.launchcmd(username))
    creds.withdraw()
    print "[WARN]: Attempting to launch, likely without the right files."
    subprocess.Popen(p.launchcmd(), shell=True)
creds=Toplevel()
creds.minsize(width=400, height=100)
UsrFrame=ttk.LabelFrame(creds, text="Username")
username=ttk.Entry(UsrFrame)
UsrFrame.pack()
username.pack()
PassFrame=ttk.LabelFrame(creds, text="Password")
password=ttk.Entry(PassFrame, show='*')
PassFrame.pack()
password.pack()
def onclose():
    creds.grab_release()
    creds.quit
creds.protocol('WM_DELETE_WINDOW', onclose)
def validate():
    invalid = """{u'errorMessage': u'Invalid credentials.', u'error': u'ForbiddenOperationException'}"""
    data = json.dumps({"agent": {"name": "Minecraft", "version": 1}, "username": username.get(), "password": password.get(), "clientToken": ""})
    headers = {'Content-Type': 'application/json'}
    r = requests.post('https://authserver.mojang.com/authenticate', data=data, headers=headers)
    output=r.json()
    print output
    try:
        file_output="%s\n%s\n%s" % (str(output["selectedProfile"]["name"]), str(output["selectedProfile"]["id"]), str(output["accessToken"]))
        win=open("usernamecache.json", "w")
        win.write(file_output)
        win.close()
        win = open("usernamecache.json", "r")
        if win.read() == invalid:
            tkMessageBox.showerror(title="Credentials Invalid.",
                                   message="It appears to be that your credentials are not valid. Please try again.")
    except:
        tkMessageBox.showerror(title="Credentials Invalid.", message="It appears to be that your credentials are not valid. Please try again.")
    else:
        onclose()
        launchMC()
def showlogin():
    creds.deiconify()
    creds.grab_set()
chk=ttk.Button(creds, text="Login", command=validate)
chk.pack()
def serverping():
    import socket
    import struct

    def unpack_varint(s):
        d = 0
        for i in range(5):
            b = ord(s.recv(1))
            d |= (b & 0x7F) << 7*i
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
        unpack_varint(s)     # Packet length
        unpack_varint(s)     # Packet ID
        l = unpack_varint(s) # String length

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
    if validate()==False:
        creds.deiconify()
        creds.grab_set()
    else:
        validate()
Frame=ttk.LabelFrame(root, text="Server Status")
Frame.pack()
var=StringVar()
ServerStatus=ttk.Label(Frame, textvariable=var)
data=serverping()
output="Server: %s\nOnline: %s" % (data["description"], data["players"]["online"])
var.set(output)
ServerStatus.pack()
Launch=ttk.Button(root, text="Launch", command=launchMC)
Launch.pack()
root.minsize(width=500, height=250)
root.mainloop()
