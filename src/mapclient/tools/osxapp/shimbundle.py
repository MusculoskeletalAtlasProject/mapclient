#!/usr/bin/env python
"""This creates an app to launch a python script so that it
appears as a genuine OS X application. A version of Python
is created via a softlink, named to match the app, which means that
the name of the app rather than Python shows up as the name in the
menu bar, etc, but this requires locating an app version of Python
(expected name .../Resources/Python.app/Contents/MacOS/Python in
directory tree of calling python interpreter).

Run this script with one or two arguments:
    <python script>
    <project name>
The script path may be specified relative to the current path or given
an absolute path, but will be accessed via an absolute path. If the
project name is not specified, it will be taken from the root name of
the script.
"""
import sys, os, stat
from subprocess import check_output
import shutil


def Usage():
    print("\n\tUsage: python " + sys.argv[0] + " appname version\n")
    sys.exit()


if not len(sys.argv) == 3:
    Usage()

version = sys.argv[2]
project = sys.argv[1]
bundleIdentifier = "org.musculoskeletalatlas.project"

# find the python application; must be an OS X app
pythonpath = check_output(['python-config', '--prefix'])
pythonapp = os.path.join(pythonpath.strip(), 'Resources', 'Python.app', 'Contents', 'MacOS', 'Python')

if not os.path.exists(pythonapp):
    print("\nSorry, failed to find a Python app in " + str(pythonapp))
    sys.exit()

apppath = os.path.abspath(os.path.join('/', 'Applications', project + ".app"))
newpython = os.path.join(apppath, "Contents", "MacOS", project)
projectversion = project + " " + version
if os.path.exists(apppath):
    try:
        shutil.rmtree(apppath)
    except:
        print("\nSorry, an app named " + project + " already exists in this location (" + str(apppath) + ")")
        print("This application will not been installed.")
        sys.exit()

os.makedirs(os.path.join(apppath, "Contents", "MacOS"))
os.makedirs(os.path.join(apppath, "Contents", "Resources"))

f = open(os.path.join(apppath, "Contents", "Info.plist"), "w")
f.write("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>English</string>
    <key>CFBundleExecutable</key>
    <string>main.sh</string>
    <key>CFBundleGetInfoString</key>
    <string>{:}</string>
    <key>CFBundleIconFile</key>
    <string>app.icns</string>
    <key>CFBundleIdentifier</key>
    <string>{:}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>{:}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>{:}</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>CFBundleVersion</key>
    <string>{:}</string>
    <key>NSAppleScriptEnabled</key>
    <string>YES</string>
    <key>NSMainNibFile</key>
    <string>MainMenu</string>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
</dict>
</plist>
""".format(projectversion, bundleIdentifier, project, projectversion, version)
        )
f.close()

# not sure what this file does
f = open(os.path.join(apppath, 'Contents', 'PkgInfo'), "w")
f.write("APPL????")
f.close()
# create a link to the python app, but named to match the project
os.symlink(pythonapp, newpython)
# create a script that launches python with the requested app
shell = os.path.join(apppath, "Contents", "MacOS", "main.sh")
# Given the current working directory this relative path should be
# correct.
program = os.path.abspath(os.path.join('..', '..', 'application.py'))
# create a short shell script
f = open(shell, "w")
f.write('#!/bin/sh\nexec "' + newpython + '" "' + program + '"\n')
f.close()
os.chmod(shell, os.stat(shell).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

shutil.copyfile(os.path.join('.', 'mapclient.icns'), os.path.join(apppath, 'Contents', 'Resources', 'app.icns'))
