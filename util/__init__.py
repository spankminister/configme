import platform

# OS X Version constants
osx_versions = {5:"Leopard",6:"Snow_Leopard",7:"Lion",8:"Mountain Lion"}


class osinfo(object):
    def __init__(self):
        macVersion = platform.mac_ver()[0].split('.')
        self.version = 0
        self.major = 0
        self.minor = 0
        print len(macVersion)
        if len(macVersion) > 0:
            self.version = macVersion[0]
        if len(macVersion) > 1:
            self.major = macVersion[1]
        if len(macVersion) > 2:
            self.minor = macVersion[2]

        try:
            self.versionName = osx_versions[int(self.major)]
        except Exception as e:
            # TODO: raise unsupported exception and handle properly
            print "Unsupported OS X version!", e
    
def getOsxVersionName():
    return versioninfo.versionName

versioninfo = osinfo()
