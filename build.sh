#!/bin/zsh
set -e
cd "$(dirname "$0")"
APP=build/DesktopMascot.app
mkdir -p $APP/Contents/MacOS
swiftc -O -o $APP/Contents/MacOS/DesktopMascot Sources/DesktopMascot/**/*.swift
cat > $APP/Contents/Info.plist <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key><string>DesktopMascot</string>
    <key>CFBundleIdentifier</key><string>local.desktop-mascot</string>
    <key>CFBundleName</key><string>DesktopMascot</string>
    <key>CFBundlePackageType</key><string>APPL</string>
    <key>LSUIElement</key><true/>
</dict>
</plist>
PLIST
echo "built $APP"
