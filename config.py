#!/usr/bin/env python

dspathmkpath = "onenotefmt.docset/Contents/Resources/Documents"
plist_file = "onenotefmt.docset/Contents/info.plist"
db_file = "onenotefmt.docset/Contents/Resources/docSet.dsidx"

plist_contents = """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleIdentifier</key>
    <string>onenotefmt</string>
    <key>CFBundleName</key>
    <string>Onenotefmt</string>
    <key>DocSetPlatformFamily</key>
    <string>onenotefmt</string>
    <key>isDashDocset</key>
    <true/>
</dict>
</plist>
"""

