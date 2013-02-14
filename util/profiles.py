import os
import os.path
import shutil

def addToFile(profile, string):
    """
    Adds the specified string to .bashrc
    """
    profile = os.path.join(os.getenv("HOME"),'.bashrc')
    bashrc = open(profile, 'a')
    bashrc.write(string)
    bashrc.write("\n")
    bashrc.close()

def addDirToPath(path):
    """
    Adds path to the PATH in .bashrc
    """
    pathline = "PATH=$PATH:%s" % path
    addToFile(os.path.join(os.getenv("HOME"),".bash_profile"),pathline)
    
def copyProfile(path):
    """
    Takes a directory/file named dot.something
    and copies it to ~/.something
    """
    filename = os.path.basename(path)
    if not filename.startswith("dot."):
        raise OperationNotSupportedException
    newfilename = filename[3:]
    targetpath = os.path.join(os.getenv("HOME"),newfilename)
    if os.path.isdir(path):
        shutil.copytree(path, targetpath)
    else:
        shutil.copy(path, targetpath)

def setupProfiles(profiledir, portagedir):
    """
    This function is the one that should be called externally
    to do the general profile setup.

    profiledir is a directory containing things like:
        dot.bash_profile
        dot.irssi/

    """
    # First copy over profiles, we may need to add things later
    # but best to start with user-supplied defaults
    for profile in os.listdir(profiledir):
        copyProfile(os.path.join(profiledir, profile))

    addDirToPath(os.path.join(portagedir,'usr','bin'))

