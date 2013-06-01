#_*_ coding:utf8 _*_
'''
'''
import urllib2
import socket
import sys
from bs4 import BeautifulSoup

class Crawler:

	def __init__(self):
		self.failedUrl = []

	def fetchPage(self, url, curPage=1):
		url = url+'&page='+str(curPage)
		try:
			html = urllib2.urlopen(url, timeout=10).read()	
		except urllib2.URLError, e:
			if isinstance(e.reason, socket.timeout):
				failedUrl.append(url)
			else:
				sys.exit(1)

				
		html = unicode(html, 'euc-kr').encode('utf-8')
		soup = BeautifulSoup(html)

		return soup

	def countPage(self, soup):
		'''
			오프라인 매장에서 총 읽어와야할 도서 갯수를 구한 후
			몇 페이지로 구성 되어었는지 계산
		'''
		roundFlag = 0
		totalNum = int(soup.find('span','ss_f_g_l').contents[0])
		pageNum = (totalNum/25)

		if totalNum%25 >= 1:
			roundFlag = 1
		
		return pageNum+roundFlag

	def makeFullUrl(self, url, page=1):
		return url+'&offcode='+offcode+'&page='+str(page)

	def extractBooksInfo(self, bookData):
		'''
			추출할 데이터 목록 
			title(+ sub title), author | publisher | publish Date
			book url, thumbnail url

			bookInfo data list =
			[ bookurl, thumbUrl, price, title, subTitle, author, publisher, publishDate ]
		'''
		try:
			bookInfo = []		
			bookInfo.append( bookData.find('a')['href'].strip() )
			bookInfo.append( bookData.find('img')['src'].strip() )
			bookInfo.append( bookData.find('span', 'ss_p3').text.strip() )
			'''
				<li>[컴퓨터/인터넷 100위 14주]</li> 가 추가 되어 있는 경우 때문에 
				index 를 뒤에서 부터 계산 
			'''
			tmpTag = bookData.find('div', 'ss_book_list').find_all('li')
			# Text Data 에서 도서명, 부재 '-'기준으로 분리
			print tmpTag[-2].text 
			if '-' in tmpTag[-2].text:
				# title과 subtitle의 구분자인 '-'가 title에 있을 경우를 대비해 
				# 뒤에서 하나만 분리 
				title, subTitle = tmpTag[-2].text.rsplit('-',1)
			else:
				title = tmpTag[-2].text
				subTitle = ' '
			bookInfo.append( title.strip() )
			bookInfo.append( subTitle.strip() )

            #print tmpTag[-1].text
			# Text Data 에서 저자, 출판사, 출판일을 '|'기준으로 분리
			# 3가지 전부 없는 경우를 대비해서 
			if tmpTag[-1].text.count('|') == 2:
				author, publisher, publishDate = tmpTag[-1].text.split('|')
			else:
				publisher, publishDate = tmpTag[-1].text.split('|')
				author = ' ' 
				
			bookInfo.append( author.strip() )
			bookInfo.append( publisher.strip() )
			bookInfo.append( publishDate.strip() )

			return bookInfo
		except:
			print 'crawler.py error!!'
			sys.exit(1)

	fetchPage = classmethod(fetchPage)
	countPage = classmethod(countPage)
	makeFullUrl = classmethod(makeFullUrl)
	extractBooksInfo = classmethod(extractBooksInfo)
