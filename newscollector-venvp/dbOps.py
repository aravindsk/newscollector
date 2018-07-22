import datetime
import pymongo
from pymongo import MongoClient
from dbConnectionProp import dbConnection



dbProp = dbConnection()
mongoClient = MongoClient(dbProp.hostPath)
mongoDb = mongoClient[dbProp.dbName]
db_articles = mongoDb.articles

def checkDBforId(articleID):
    countRowsForID = db_articles.count({"_id":articleID})
    if countRowsForID == 0:
        return False
    else:
        return True
    

def upsertToDB(entryDict):
    updateResult = db_articles.update_one({'_id':entryDict['_id']}, 
                                            {'$set': {
                                                        'logUpdateTime' : (datetime.datetime.utcnow())
                                                    }
                                            ,
                                                '$setOnInsert': {
                                                                'source':entryDict['source_site'],
                                                                'articleText' : entryDict['articleText'],
                                                                'title' : entryDict['title'],
                                                                'published' : entryDict['published'],
                                                                'summary':entryDict['summary'],
                                                                'link' : entryDict['link'],
                                                                'logInsertTime' : (datetime.datetime.utcnow())
                                                                }
                                            
                                            },
                                            upsert=True , collation=None, array_filters=None)
    print(updateResult)