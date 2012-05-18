#!/home/jake/.virtualenvs/default/bin/python

import urllib2
import re
from subprocess import Popen, PIPE, STDOUT


bad_links = ['http://imslp.org/wiki/Category:Arrangers',
             'http://imslp.org/wiki/Category:Composers',
             'http://imslp.org/wiki/Category:Editors',
             'http://imslp.org/wiki/Category:Librettists',
             'http://imslp.org/wiki/Category:People',
             'http://imslp.org/wiki/Category:People_by_nationality',
             'http://imslp.org/wiki/Category:Performers',
             'http://imslp.org/wiki/Category_talk:People',
             'http://imslp.org/wiki/Category:Translators',
             'http://imslp.org/wiki/Category:WIMA_files']

for url in open('composition_lists.txt'):
    get_links = ['lwp-request', '-o', 'links', url]
    p = Popen(get_links, shell=False, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    output = p.stdout.read()
    links = re.findall(r'http://imslp.org/wiki/Category:.*', output)
    people_pages = [x for x in links if x not in bad_links]
    for link in people_pages:
        print link
