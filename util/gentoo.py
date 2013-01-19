import os
import subprocess

# Gentoo module provides:
#   * Wrapper for the setupPortage script
#   * A wrapper for emerge
# Seems like an odd way to do this, but bootstrapping portage is
# easier to verify and maintain as "black box" bash script than as a Pythony
# process: translating the official instructions turned out to be more error prone
# due to environment, etc.

def emerge(package=None, oneshot=False, nodeps=False):
    """
    Wrapper around emerge.
    """
    if package == None:
        raise Exception("Must specify a package to emerge!")

    cmd = ["emerge"]
    if oneshot:
        cmd.append("--oneshot")
    if nodeps:
        cmd.append("--nodeps")
    cmd.append(package)
    proc = subprocess.Popen(cmd, shell=True, bufsize=1, 
                     stdin=subprocess.PIPE, 
                     stdout=subprocess.PIPE, 
                     stderr = subprocess.PIPE)
    (out, unused_err) = proc.communicate()

def bootstrapGentooPrefix(prefixPath=None):
    # FIXME: make a separate function for the bootstrap_prefix stuff
    """
    Should do all the Gentoo Prefix setup required as described in:
        http://www.gentoo.org/proj/en/gentoo-alt/prefix/bootstrap-macos.xml

    Basic steps:
        * Install base for bootstrap (bootstrap_prefix script)
        * Emerge oneshots for temporary bootstrap portage
        * Emerge real portage on top of bootstrapped portage
        * Emerge sync
        * Emerge system to update prefix packages
        * Set USE and CFLAGS
        * Re-emerge system with new settings/environment.
    """
    # If no prefixpath is specified, use the default of ~/Gentoo
    if prefixPath == None:
        prefixPath = os.path.join(os.getenv('HOME'), "Gentoo")

    cmd = os.path.join(os.getcwd(),"util","setupPortage.sh") 
    #cmd = cmd + " " + prefixPath
    #print cmd
    cmd = [cmd, prefixPath]
    print cmd
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    (out, unused_err) = proc.communicate()
    print out
    print unused_err

    #os.system(cmd + " " + prefixPath)
    #proc = subprocess.Popen([cmd,prefixPath], shell=False, bufsize=4096)
    # TODO: Actually use some logging or something for the child process
    #(out, unused_err) = proc.communicate()

