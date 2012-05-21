#!/home/jake/.virtualenvs/default/bin/python
import os
import urllib2
import lxml.html
import re
from subprocess import call

ROOT_DIR = os.path.join(os.getcwd(), 'people')

def parse_html(html):
    return lxml.html.fromstring(open(html).read())

def get_item_links(parsed_html):
    return [x[2] for x in parsed_html.iterlinks() if 'pdf' in x[2] and 'images' in x[2]]

for dir in os.listdir('people'):
    os.chdir(ROOT_DIR)
    ITEM_DIR = os.path.join(ROOT_DIR, dir)
    os.chdir(ITEM_DIR)
    for file in os.listdir('.'):
        if file.endswith('scores.html'):
            file = os.path.join(ITEM_DIR, file)
            parsedhtml = parse_html(file)
            item_links = get_item_links(parsedhtml)
            for pdf in item_links:
                pdf_url = 'http://imslp.org%s' % pdf
                wget = "wget -q -nc --header='Cookie: imslpdisclaimeraccepted=yes' %s" % pdf_url
                call(wget, shell=True)
                with open('map.txt', 'a') as mf:
                    mf.write(file + '\t' + pdf_url + '\n')
                print "SUCCESSS :: %s\t%s" % (dir, pdf_url)
