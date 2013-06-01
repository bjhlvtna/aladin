#-*- coding:utf8 -*-
'''

'''
import MySQLdb
import sys

class DB:
    # SQLITE3 wrapper class
    def __init__(self):
        self.conn = MySQLdb.connect(db='crawlerDB', user='root', passwd='mysql84',charset="utf8")
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

	# Seed table에서 seed가 될 url을 읽어 온다.
    # row[1] << 이 부분 수정
    def selectCrawlSeed(self):
    	self.cursor.execute('SELECT * FROM seed')
    	return [ row[1] for row in self.cursor.fetchall() ]


    # crawling 후 업데이트 안된 데이터들 삭제 ( 기준 regTime < current date )
    def deleteSoldoutBookInfo(self):
        try:
            self.cursor.execute("DELETE FROM document WHERE updateTime<>UTC_DATE()")
            self.conn.commit() 
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
        else:
            return 1

    def selectBookInfo(self):

        try:
            self.cursor.execute("SELECT * FROM document")
            rows = self.cursor.fetchall()
        except:
            return None
        else:
            return rows


    # 데이터 입력 & 저장되어 있는 데이터의 경우 regTime 업데이트
    def insertBookInfo(self, bookInfo):
        
        try:
            bookUrl = bookInfo[0].encode('utf8')
            thumbUrl = bookInfo[1].encode('utf8')
            price = bookInfo[2].encode('utf8')
            title = self.conn.escape_string(bookInfo[3].encode('utf8'))
            subTitle = self.conn.escape_string(bookInfo[4].encode('utf8'))
            author = self.conn.escape_string(bookInfo[5].encode('utf8'))
            publisher = self.conn.escape_string(bookInfo[6].encode('utf8'))
            publishDate = bookInfo[7].encode('utf8')
            offcode = bookInfo[8].encode('utf8')
            
            self.cursor.execute("INSERT INTO document VALUES \
                ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', curdate(), curdate() )"%(bookUrl, thumbUrl, price, title, subTitle, author, publisher, publishDate, offcode))
            self.conn.commit()
        except MySQLdb.IntegrityError:
            self.cursor.execute("UPDATE document set updateTime=curdate() where (bookUrl='%s' and offcode='%s')"%(bookUrl, offcode) )
            #self.conn.commit()
            #print 'Duplicate BookInfo'
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
        else:
            return 1
        






