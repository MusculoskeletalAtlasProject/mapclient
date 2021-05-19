#!/bin/sh
version=0.15.0
test -f MAP-Client-$version.dmg && rm MAP-Client-$version.dmg
#  --volicon "application_icon.icns" \
create-dmg \
  --volname "MAP-Client-$version" \
  --background "map-client-dmg-background.png" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "MAP-Client.app" 200 190 \
  --hide-extension "MAP-Client.app" \
  --app-drop-link 600 185 \
  "MAP-Client-$version.dmg" \
  "../pyinstaller/dist/"

