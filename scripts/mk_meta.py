#!/home/jake/.virtualenvs/default/bin/python
import os
import urllib2
import lxml.html
import base64
import re
import simplejson as json
from subprocess import call

ROOT_DIR = os.path.join(os.getcwd(), 'people')
mkdir = lambda x: os.makedirs(x) if not os.path.exists(x) else None


#______________________________________________________________________________
def parse_html(html):
    return lxml.html.fromstring(open(html).read())

#______________________________________________________________________________
def get_json(parsed_html):
    rmtitle = ' - IMSLP/Petrucci Music Library: Free Public Domain Sheet Music'
    title = parsedhtml.cssselect('title')[0].text_content().replace(rmtitle, '').encode('utf-8')
    id = base64.b64encode(title)
    query_url = ('http://imslp.org/imslpscripts/API.ISCR.php?'
                 'retformat=json/'
                 'disclaimer=accepted/'
                 'type=0/'
                 'id=%s' % id)
    return json.loads(urllib2.urlopen(query_url).read())

#______________________________________________________________________________
def get_pdf_names(parsed_html):
    return [x[2].split('/')[-1] for x in parsed_html.iterlinks() if 'pdf' in
            x[2] and 'images' in x[2]]

#______________________________________________________________________________
def get_date(jstor):
    bstor = jstor['extvals']
    try:
        if bstor['Year/Date of Composition']:
            return bstor['Year/Date of Composition']
        if bstor['Year of First Publication']:
            return bstor['Year of First Publication']
        if bstor['First Performance']:
            return bstor['First Performance']
        else:
            return None
    except KeyError:
        return None

#______________________________________________________________________________
def mk_meta_dict(parsed_html, file):
    src = "http://imslp.org/index.php?oldid=%s" % file.replace('_scores.html','')
    jstor = get_json(parsedhtml)[0]
    date = get_date(jstor)
    try:
        subjects = jstor['intvals']['rawtagcats'].replace('|',';')
        key = jstor['extvals']['Key']
    except KeyError:
        subjects = None
        key = None
    meta_dict = {'subject': subjects,
                 'collection': 'imslp',
                 'call_number': jstor['extvals']['Opus/Catalogue Number'],
                 'language': jstor['extvals']['Language'],
                 'piece_style': jstor['extvals']['Piece Style'],
                 'instrumentation': jstor['extvals']['Instrumentation'],
                 'librettist': jstor['extvals']['Librettist'],
                 'dedication': jstor['extvals']['Dedication'],
                 'movements': jstor['extvals']['Number of Movements/Sections'],
                 'comments': jstor['extvals']['*****COMMENTS*****'],
                 'key': key,
                 'mediatype': 'texts',
                 'date': date,
                 'source': src,
                 'title': jstor['intvals']['worktitle'],
                 'creator': jstor['intvals']['composer'],
                 }
    return {k: v for k,v in meta_dict.iteritems() if v}

#______________________________________________________________________________
for dir in os.listdir('people'):
    ITEM_DIR = os.path.join(ROOT_DIR, dir)
    os.chdir(ITEM_DIR)
    for file in os.listdir('.'):
        if file.endswith('scores.html'):
            parsedhtml = parse_html(file)
            meta_dict = mk_meta_dict(parsedhtml, file)
            identifier = "imslp-%s" % file.replace('_scores.html', '')
            final_item_dir = '/1/incoming/tmp/imslp/%s' % identifier
            pdf_files = [os.path.join(ITEM_DIR, x) for x in get_pdf_names(parsedhtml)]
            mkdir(final_item_dir)
            os.chdir(final_item_dir)

            # LOGGING
            #__________________________________________________________________
            if not meta_dict.get('date'):
                print "WARNING :: NO DATE\t%s\t%s" % (identifier, ITEM_DIR)
            if not meta_dict.get('title'):
                print "WARNING :: NO TITLE\t%s\t%s" % (identifier, ITEM_DIR)
            if len(pdf_files) >= 10:
                print "WARNING :: TOO MANY PDFs\t%s\t%s" % (identifier, ITEM_DIR)
