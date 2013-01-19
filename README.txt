ConfigMe: Simple, low overhead setup of OS X workstations.

Usage:
Run once as superuser:
    sudo python install.py
Run once as main user:
    python install.py

What to know:
    * Running as superuser will install OS updates, apps, disable Spotlight, etc.
    * Running as regular user will install the package manager.
    * The package manager will end up using its own overlay for ls, python, etc.

================ Prerequisites ==================
* IMPORTANT: Assumes you're using gcc 4.2.1
* Install OS X of your choice
* Install XCode and command line tools
    * For Lion, go to App Store, download XCode
    * Run XCode, accept license agreement
    * Go to XCode->Preferences, Downloads tab.
    * Install command line tools

Now, setup your directory structure as follows:
APPDIR:
    MacPorts/
        Leopard/
            SomeMacPorts.x.dmg
        Tiger/
            SomeMacPorts.y.dmg
    autoinstall/
        someapp1/
            someapplication1.dmg
        someapp2/
            someapplication2.mpkg

Then, run 'python install.py'

====================================================
