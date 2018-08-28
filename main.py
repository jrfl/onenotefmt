#!/usr/bin/env python

import os
from config import dspathmkpath
from config import plist_file
from config import plist_contents

if not os.access(dspathmkpath, os.R_OK | os.W_OK):
    os.makedirs(dspathmkpath)

with open(plist_file, 'w') as f:
    f.write(plist_contents)

