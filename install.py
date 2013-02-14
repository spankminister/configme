import sys
import os
import os.path
import platform
import subprocess
import signal
import munkilib
import munkilib.installer
import munkilib.appleupdates

import glob

import util
import util.gentoo
import util.profiles

VERBOSE = False

if VERBOSE:
    OUTPUT = None
else:
    OUTPUT = subprocess.PIPE

# =========== Configure this section for your system ============
PORTS = [   "nmap",
            "metasploit3",
            "wget",
            "w3m",
            "unrar",
            "python26",
            "py26-pygresql",
            "postgresql90",
            "python32",
            "irssi",    ]

                   
# Set to the base directory with all the apps/profiles you want installed
APPDIR = "/Volumes/apps/OSX/"

# ========== END CONFIG SECTION ========================
AUTOINSTDIR = os.path.join(APPDIR, "autoinstall")
PROFILEDIR = os.path.join(APPDIR, "profiles")
PORTAGEDIR = os.path.join(os.getenv("HOME"),"Gentoo")
# ==============================================================

def signal_handler(signal, frame):
    print "Caught CTRL+C, aborting."
    sys.exit(0)

def installPackagesInDir(dirpath):
    # Check for the existence of OS-specific directory name?
    os_specific_dir = os.path.join(dirpath, util.getOsxVersionName())
    #print "Checking for directory %s" % os_specific_dir
    # If there's a specific subdirectory for this version of OS X, use it
    if os.path.exists(os_specific_dir):
        dirpath = os_specific_dir
    print "Attempting to run installer on %s" % dirpath
    for f in os.listdir(dirpath):
        if f.endswith('.dmg') and not f.startswith('.'):
            print "Found a dmg at: %s" % os.path.join(dirpath, f)
            result = munkilib.installer.copyAppFromDMG(os.path.join(dirpath, f)) 
            if result == -2:
                # Failed to find an app, let's try a package instead
                # FIXME: Right now, I don't think this works
                retcode, reboot = munkilib.installer.installall(dirpath)

#FIXME: Easy refactoring here for calling subprocesses
                
def installMacPort(portname):
    # No longer maintained or supported since I don't use it.
    cmd = ["/opt/local/bin/port", "install", portname]
    proc = subprocess.Popen(cmd, shell=False, bufsize=1, 
                     stdin=subprocess.PIPE, 
                     stdout=subprocess.PIPE, 
                     stderr = subprocess.PIPE)
    (out, unused_err) = proc.communicate()

def installAppleUpdates():
    # Just a wrapper around Apple's builtin "softwareupdate" command-line tool
    cmd = ["/usr/sbin/softwareupdate", "-i", "-a"]
    proc = subprocess.call(cmd, stdout=OUTPUT)

def disableSpotlight():
    """
    Future work can do this all the different ways that other versions of OSX require.
    """
    # TODO: Replace with call to subprocess, mask output since it's boring.
    os.system("mdutil -a -i off")

def setupConfigDir():
    configdir = os.path.expanduser("~/.configme")
    if not os.path.exists(configdir):
        os.makedir(configdir)
    
def main(argv = sys.argv):
    # Get OS version
    print "OS X Version appears to be: %s" % util.getOsxVersionName()

    signal.signal(signal.SIGINT, signal_handler)

    # We install different things depending on whether or not
    # the script has been run as root.
    isRoot = (os.geteuid() == 0)

    if isRoot:
        print "##### RUNNING AS SUPERUSER #####"
        # Stuff to be done as superuser
        print "* Disabling Spotlight: ",
        disableSpotlight()
        print "[DONE]"

        # Install Apple updates
        print "* Installing Apple Updates: ",
        installAppleUpdates()
        #os.system("softwareupdate -i -a")
        print "[DONE]"

        # Install the apps
        print "* Installing other programs: ",
        print glob.glob(os.path.join(AUTOINSTDIR, "*"))
        for entry in glob.glob(os.path.join(AUTOINSTDIR, "*")):
            if os.path.isdir(entry):
                print "******"
                print entry
                print "******"
                installPackagesInDir(entry)
        print "[DONE]"

    else:
        # Stuff to be done as regular user
        # Install Gentoo Prefix
        print "##### Running as user TODO #####"
        print "* Bootstrapping Gentoo Prefix"
        #util.gentoo.bootstrapGentooPrefix(PORTAGEDIR)

        # Copy and install appropriate profiles
        util.profiles.setupProfiles(PROFILEDIR,PORTAGEDIR)
        return
        #FIXME: Remove return above

if __name__ == '__main__':
    sys.exit(main())


