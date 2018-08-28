#!/usr/bin/env python

import os
import re
import sqlite3
from bs4 import BeautifulSoup as bs4
from config import db_file

ndxfile = "dd953044(v=office.12).aspx"

conn = sqlite3.connect(db_file)
cur = conn.cursor()

try:
    cur.execute('DROP TABLE searchIndex;')
except Exception:
    pass

cur.execute('''CREATE TABLE
               searchIndex(id INTEGER PRIMARY KEY,
               name TEXT,
               type TEXT,
               path TEXT);
               ''')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpath = 'onenotefmt.docset/Contents/Resources/Documents'

page = open(os.path.join(docpath, ndxfile)).read()
soup = bs4(page, features="lxml")

any = re.compile('.*')
for tag in soup.find_all('a', {'href': any}):
    name = tag.text.strip().replace("\n", " ")
    namel = name.lower()
    kind = ""

    if namel == "vendor-extensible fields":
        continue

    if namel.find("structure") > -1:
        # name = name.replace("structure", "").strip()
        kind = 'Struct'
    elif namel.find("array") > -1:
        kind = 'Type'
    elif namel == "version history page":
        kind = 'Guide'
    elif namel == "character position (cp)":
        kind = 'Guide'
    elif namel == "section":
        kind = 'Guide'
    elif namel == "references":
        kind = 'Guide'
    elif namel == "page":
        kind = 'Guide'
    elif namel.find("simple types") > -1:
        kind = 'Guide'
    elif namel.find("fundamental concepts") > -1:
        kind = 'Guide'
    elif namel.find("implementer") > -1:
        kind = 'Guide'
    elif namel.find("change tracking") > -1:
        kind = 'Guide'
    elif namel.find("tracking changes") > -1:
        kind = 'Guide'
    elif namel.find("- overview") > -1:
        kind = 'Guide'
    elif namel.find("example") > -1:
        kind = "Guide"
    elif namel == "applicability":
        kind = "Guide"
    elif namel == "glossary":
        kind = "Guide"
    elif namel == "introduction":
        kind = "Guide"
    elif namel.find("complex types") > -1:
        kind = 'Guide'
    elif namel.find("properties") > -1:
        kind = 'Guide'
    elif namel.find("property sets") > -1:
        kind = 'Guide'
    elif namel.find("overview") > -1:
        kind = 'Guide'
#    elif namel.find("jcid") == 0:
#        kind = 'Type'
#    elif namel.find("node") > -1:
#        kind = 'Type'
    else:
        kind = 'Type'
        # print("Different Type:", name)

    if len(name) > 1:
        path = "./" + tag.attrs['href'].strip()
        if path != ndxfile:
            if len(kind) == 0:
                print('name: %s, path: %s, kind: %s' % (name, path, kind))
            else:
                cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path)\
                            VALUES (?,?,?)',
                            (name, kind, path))

conn.commit()
conn.close()
