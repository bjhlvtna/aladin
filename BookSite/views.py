# -*- coding: utf8 -*-
# Create your views here.


from django.http import HttpResponse

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient
#for template
from django.template import Context, loader

from BookSearcher import BookSearcher

listSize = 10
showLength = 100

def main_page(req):
	tpl = loader.get_template('main.html')
	ctx = Context({ })
	html = tpl.render(ctx)
	return HttpResponse(html)

def SearchPage(req, keyword, page=1): # req : request
    global listSize
    page = int(page)
    try:
        bs = BookSearcher()
        resultDic = bs.TotalSearch(keyword)
        
    except:
        print 'Django-views-SearchPage'
        exit(1)
    
    searchList = resultDic[((page-1)*listSize):(page*listSize)]

    totalSize = len(resultDic)       
    pageCnt = totalSize / listSize
    if (totalSize % listSize ) != 0 :
	      pageCnt += 1
    
    pageList = range(1, pageCnt + 1)

    tpl = loader.get_template('search.html')  
    ctx = Context({ 
    		'searchList' : searchList,         
    		'keyword' : keyword,
    		'pageList' : pageList,
    })
    
    html = tpl.render(ctx)
    return HttpResponse(html)


def LatestPage(req, page=1):
    global listSize
    page = int(page)
    try:
        bs = BookSearcher()
        resultDic = bs.LatestSearch()
    except:
        print 'Django-views-Latestpage'
        exit(1)
    
    searchList = resultDic[((page-1)*listSize):(page*listSize)]
    totalSize = len(resultDic)       
    pageCnt = totalSize / listSize
    if (totalSize % listSize ) != 0 :
          pageCnt += 1
    
    pageList = range(1, pageCnt + 1)
    
    tpl = loader.get_template('search.html')  
    ctx = Context({ 
        
            'searchList' : searchList,         
            'keyword' : ' ',
            'pageList' : pageList,
    })
    
    html = tpl.render(ctx)
    return HttpResponse(html)

def evernote(req):
    imgurl = req.GET['imgurl']
    title = req.GET['title']
    title = "트위터, 140문자가 세상을 바꾼다"
    auth_token = "S=s1:U=6bc25:E=146546e6e47:C=13efcbd4249:P=1cd:A=en-devtoken:V=2:H=eafbf063b51f5fef898e8cc1add8a3c6"

    if auth_token == "your developer token":
        print "Please fill in your developer token"
        print "To get a developer token, visit " \
            "https://sandbox.evernote.com/api/DeveloperToken.action"
        exit(1)

    # Initial development is performed on our sandbox server. To use the production
    # service, change sandbox=False and replace your
    # developer token above with a token from
    # https://www.evernote.com/api/DeveloperToken.action
    client = EvernoteClient(token=auth_token, sandbox=True)

    user_store = client.get_user_store()

    version_ok = user_store.checkVersion(
        "Evernote EDAMTest (Python)",
        UserStoreConstants.EDAM_VERSION_MAJOR,
        UserStoreConstants.EDAM_VERSION_MINOR
    )
    print "Is my Evernote API version up to date? ", str(version_ok)
    print ""
    if not version_ok:
        exit(1)

    note_store = client.get_note_store()

    # List all of the notebooks in the user's account
    notebooks = note_store.listNotebooks()
    print "Found ", len(notebooks), " notebooks:"
    for notebook in notebooks:
        print "  * ", notebook.name

    print
    print "Creating a new note in the default notebook"
    print

    # To create a new note, simply create a new Note object and fill in
    # attributes such as the note's title.
    note = Types.Note()
    note.title = title

    # To include an attachment such as an image in a note, first create a Resource
    # for the attachment. At a minimum, the Resource contains the binary attachment
    # data, an MD5 hash of the binary data, and the attachment MIME type.
    # It can also include attributes such as filename and location.
    image = open('/Users/loading/Dropbox/project/python/UsedBookSite/BookSite/book2.png', 'rb').read()
    md5 = hashlib.md5()
    md5.update(image)
    hash = md5.digest()

    data = Types.Data()
    data.size = len(image)
    data.bodyHash = hash
    data.body = image

    resource = Types.Resource()
    resource.mime = 'image/png'
    resource.data = data

    # Now, add the new Resource to the note's list of resources
    note.resources = [resource]

    # To display the Resource as part of the note's content, include an <en-media>
    # tag in the note's ENML content. The en-media tag identifies the corresponding
    # Resource using the MD5 hash.
    hash_hex = binascii.hexlify(hash)

    # The content of an Evernote note is represented using Evernote Markup Language
    # (ENML). The full ENML specification can be found in the Evernote API Overview
    # at http://dev.evernote.com/documentation/cloud/chapters/ENML.php
    note.content = '<?xml version="1.0" encoding="UTF-8"?>'
    note.content += '<!DOCTYPE en-note SYSTEM ' \
        '"http://xml.evernote.com/pub/enml2.dtd">'
    note.content += '<en-note>' + title + '<br/>'
    note.content += '<en-media type="image/png" hash="' + hash_hex + '"/>'
    note.content += '</en-note>'

    # Finally, send the new note to Evernote using the createNote method
    # The new Note object that is returned will contain server-generated
    # attributes such as the new note's unique GUID.
    created_note = note_store.createNote(note)

    print "Successfully created a new note with GUID: ", created_note.guid
    return HttpResponse("ok")

