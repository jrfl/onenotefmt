#!/usr/bin/env python

from requests import Session
from bs4 import BeautifulSoup as bs4
import concurrent.futures as cf
import re
from config import dspathmkpath

quiet = True
mainurl = "https://msdn.microsoft.com/en-us/library/dd924743(v=office.12).aspx"
pth = 'https://msdn.microsoft.com/en-us/library/'
headersb = "\n".join([
    '''<html dir="ltr" lang="en">''',
    '''<head>''',
    '''<meta charset="utf-8" />''',
    '''<title>[MS-ONE]: OneNote File Format</title>''',
    '''</head>''',
    '''<body class="library" style="font-size:smaller;">'''
])

headerse = "\n".join([
    '''</body>''',
    '''</html>'''
])


def preproc(url, to=60):
    ''' Fetch the HTML and remove some cruft '''
    r = session.get(url, timeout=to)
    if r.status_code == 200:
        # r.html.pq.remove_namespaces()
        return r
    else:
        raise Exception("Fetch of {} failed with HTTP status code {}".
                        format(url, r.status_code))


def collecturls(urls, pq):
    ''' Extract the links to further content pages '''
    added = False
    for t in pq('.toclevel2'):
        urls.append(t[0].attrib['href'])
        added = True

    return added


def mungeData(h):
    ''' Remove some of the crap ms injects into the HTML '''
    for i in h.find_all('div', {'class': 'libraryMemberFilter'}):
        i.extract()

    for i in h.find_all('div', {'class': 'lw_vs'}):
        i.extract()

    for i in h.find_all('div', {'style': 'clear:both;'}):
        i.extract()

    for i in h.find_all('div', {'id': 'archiveDisclaimerText'}):
        i.extract()

    for i in h.find_all('div', {'style': 'archiveDisclaimerText'}):
        i.extract()

    for i in h.find_all('input',
                        {'id': 'libraryMemberFilterEmptyWarning'}):
        i.extract()


def writeData(filename, soup):
    global pat
    global substs
    global replace

    with open(dspathmkpath + "/" + filename, "w") as f:
        soup = soup.find_all('div', {"class": "content"})[0]
        mungeData(soup)
        out = re.sub(pat, replace, soup.decode_contents())
        out = "\n".join([headersb,  out, headerse])
        f.write(out)


def linkFinder(links, bsoup):
    items = bsoup.findAll('div', {'class': 'toclevel2'})
    for i in items:
        for x in i.findAll('a'):
            links.append(x['href'])


maxRetry = 10
urls = []
results = dict()
errors = dict()


print("This script can take a while especially on a slow net connection")
print("Supposedly, good things come to those who wait... :) /s")
session = Session()
r = preproc(mainurl)

soup = bs4(markup=r.content, features="lxml")
results[mainurl] = soup
del r

linkFinder(urls, soup)

# with cf.ThreadPoolExecutor(max_workers=5) as executor:
with cf.ThreadPoolExecutor(max_workers=8) as executor:
    cnt = 1
    while 1:
        # Load up the batch of urls to fetch
        futures = {executor.submit(preproc, url, 60):
                   url for url in urls if url not in results}
        futures2 = []
        # For each fetched url
        for future in cf.as_completed(futures):
            url = futures[future]
            try:
                data = future.result()
            except Exception as exc:
                err = errors[url]
                err += 1
                errors[url] = err
                print('%r generated an exception: %s.  (%d of %d)' %
                      (url, exc, err, maxRetry))
                if err < maxRetry:
                    urls.append(url)  # resubmit here
            else:
                if url in results:
                    print('DUPLICATE: {}'.format(url))
                else:
                    if not quiet:
                        print('%03d: %r: %d' % (cnt, url, data.status_code))
                    cnt += 1
                    soup2 = bs4(markup=data.content, features="lxml")
                    del data
                    results[url] = soup2
                    linkFinder(futures2, soup2)
        if len(futures2) == 0:
            break
        else:
            urls = list(set(futures2))

# The following 3 statements build a regex replace string
# that cannot be built until this point.  It is built here
# in order to be efficient.  pat, substs and replace are
# referred to in mungeData
pat = "|".join('(%s)' % re.escape(pth + p.split("/")[-1])
               for p in results.keys())

substs = [p.split("/")[-1] for p in results.keys()]
replace = lambda m: substs[m.lastindex - 1]

for k, i in results.items():
    d = results[k]
    fname = k.split("/")[-1]
    if not quiet:
        print("Writing out:", fname)
    writeData(fname, d)

print('{} Items.\nDone'.format(cnt))
