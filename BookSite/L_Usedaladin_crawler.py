#_*_ coding:utf8 _*_
'''
'''
import time, sys
from db import DB
from crawler import Crawler 
from BookSearcher import BookSearcher

offcode = ['gangnam','jongno','daehakro','sinchon']

def makeSeedUrl(seed, offcode):

	newSeed = []
	for seed in seedUrl:
		for code in offcode:
			newSeed.append(seed+'&offcode='+code)

	return newSeed


if __name__ =='__main__':
	# seed url 가져오기

    db = DB()
    c = Crawler()

    try:
		seedUrl = db.selectCrawlSeed() 
		seedUrl = makeSeedUrl(seedUrl, offcode)

		for cnt, seed in enumerate(seedUrl, 0):
			# 해당 페이지 읽어 오기 
			soup = c.fetchPage(seed)
			totalPageNum = c.countPage(soup)+1
			
			for curPage in range(1,totalPageNum):
				print 'Seed : ' + seed
				time.sleep( 2 )
				soup = c.fetchPage(seed, curPage)		
				booksData = soup.find_all('div', 'ss_book_box')

				for bookData in booksData:
					bookInfo = c.extractBooksInfo(bookData)
					bookInfo.append(offcode[cnt])
					db.insertBookInfo(bookInfo)

		print 'Crawling Complete!!'

    except:
		print 'Crawling Failed!!'
		sys.exit(1)
    else:
		# indexing 
		db.deleteSoldoutBookInfo()
		rows = db.selectBookInfo()
		indexer = BookSearcher(rows)
		indexer.UpdateIndex()

		print 'Indexing Complete!!'


