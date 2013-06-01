#_*_ coding:utf8 _*_
'''
'''
import sys
import time
import lucene
from lucene import Version, File, SimpleFSDirectory \
    , IndexSearcher, QueryParser

INDEX_DIRECTORY = '../BooksIndex'

class BookSearcher:

    def __init__(self, rows=None):
        #lucene.initVM()
        # Django의 setttings.py 에 lucene.initVM() 설정 후 불러다 사용
        vm_env = lucene.getVMEnv()
        if vm_env == None:
            lucene.initVM()
        else:
            vm_env.attachCurrentThread()
        self.analyzer = lucene.StandardAnalyzer(Version.LUCENE_30)
        self.indexDir = SimpleFSDirectory(File(INDEX_DIRECTORY))
        self.rows = rows

    def UpdateIndex(self):
        # 인덱스를 최신 내용으로 갱신
        writer = lucene.IndexWriter(self.indexDir, self.analyzer, True, lucene.IndexWriter.MaxFieldLength(512))
        
        try:
            # DB에서 내용 가져오기 
            for row in self.rows:
                doc = lucene.Document()
        
                doc.add(lucene.Field("bookUrl", row[0], lucene.Field.Store.YES, lucene.Field.Index.NO ))
                doc.add(lucene.Field("thumbUrl", row[1], lucene.Field.Store.YES, lucene.Field.Index.NO ))
                doc.add(lucene.Field("price", row[2], lucene.Field.Store.YES, lucene.Field.Index.NO ))
                doc.add(lucene.Field("title", row[3], lucene.Field.Store.YES, lucene.Field.Index.ANALYZED ))
                doc.add(lucene.Field("subTitle", row[4], lucene.Field.Store.YES, lucene.Field.Index.NO ))
                doc.add(lucene.Field("author", row[5], lucene.Field.Store.YES, lucene.Field.Index.ANALYZED ))
                doc.add(lucene.Field("publisher", row[6], lucene.Field.Store.YES, lucene.Field.Index.ANALYZED ))
                doc.add(lucene.Field("publishDate", row[7], lucene.Field.Store.YES, lucene.Field.Index.NO ))
                doc.add(lucene.Field("offcode", row[8], lucene.Field.Store.YES, lucene.Field.Index.ANALYZED ))
                date = str(row[9]).split('-')
                date = ''.join(date)
                print 'regDate : '+date + ' ' + str(type(date))
                doc.add(lucene.Field("regDate", date, lucene.Field.Store.YES, lucene.Field.Index.ANALYZED ))

                date = str(row[10]).split('-')
                date = ''.join(date)
                print 'updateDate : '+date
                doc.add(lucene.Field("updateDate", date, lucene.Field.Store.YES, lucene.Field.Index.ANALYZED ))
                
                writer.addDocument(doc)
        except Exception, e:
            print "Failed in adding index : %s"%e
            exit(1)

        writer.optimize()
        writer.close()

    def packedData(self, resultList):
        print 'pack' 
        try:
            for index, result in enumerate(resultList):
                packedList = []
                bookUrl = result['bookUrl']
                price = result['price']
                offcode = result['offcode']
                
                for idx in range(len(bookUrl)):
                    dic = {}
                    dic['bookUrl'] = bookUrl[idx]
                    dic['price'] = price[idx]
                    dic['offcode'] = offcode[idx]
                    packedList.append(dic)
                
                resultList[index].update({'pack':packedList})
        except Exception, err:
            sys.stderr.write("ERROR: %s\n"% str(err))

        print resultList[0]['pack']
        return resultList
    
    def reduceDuplication(self, resultDic):
        keyList = []
        newResult = []
        
        print 'reduce Duplication'
        for result in resultDic:
            if result['title'] in keyList:
                idx = keyList.index(result['title'])
                newResult[idx]['bookUrl'].append(result['bookUrl'][0])
                newResult[idx]['price'].append(result['price'][0])
                newResult[idx]['offcode'].append(result['offcode'][0])
            else:
                keyList.append(result['title'])
                newResult.append(result)
        print 'end reduce'        
        return newResult

    def __MakeResultFormat(self, hits, searcher):
        ret = []
        offline = {'gangnam':'강남점','jongno':'종로점', 'daehakro':'대학로점', 'sinchon':'신촌점'}
        print 'makeresultformat'
        for hit in hits.scoreDocs:
            dic = {}
            doc = searcher.doc(hit.doc)
            dic['isbn'] = doc.get('bookUrl').split('?')[1].split('=')[1]
            dic['bookUrl'] = [doc.get('bookUrl')+'&offcode='+doc.get('offcode')]
            dic['thumbUrl'] = doc.get('thumbUrl')
            dic['price'] = [doc.get('price').replace('최저가','중고가')]
            dic['title'] = doc.get('title')
            dic['subTitle'] = doc.get('subTitle')
            dic['author'] = doc.get('author')
            dic['publisher'] = doc.get('publisher')
            dic['publishDate'] = doc.get('publishDate')
            dic['offcode'] = [offline[doc.get('offcode')]]
            dic['regDate'] = doc.get('regDate')
            dic['updateDate'] = doc.get('updateDate')
            
            ret.append(dic)

        searcher.close()
        ret = self.reduceDuplication(ret)
        return self.packedData(ret)


    def TotalSearch(self, keyWord):
        try:
            searcher = IndexSearcher(self.indexDir)
            keyWord = keyWord.encode('utf8')
            query = QueryParser(Version.LUCENE_30, "title", self.analyzer).parse(keyWord)
            
            hits = searcher.search(query, 1000)
            return self.__MakeResultFormat(hits, searcher)
        except Exception, err:
            sys.stderr.write("ERROR: %s\n"% str(err))
        except:
            print 'BookSearcher TotalSearch Exception'

    def LatestSearch(self):
        try:
            searcher = IndexSearcher(self.indexDir)
            today = time.strftime('%Y%m%d')
            keyWord = today.encode('utf8')
            print keyWord
            query = QueryParser(Version.LUCENE_30, "regDate", self.analyzer).parse(keyWord)

            hits = searcher.search(query, 1000)
            return self.__MakeResultFormat(hits, searcher)
        except:
            print 'BookSearcher TotalSearch Exception'




