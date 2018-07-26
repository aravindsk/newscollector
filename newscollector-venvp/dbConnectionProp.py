class dbConnection(object):
    def __init__(self):
        # self.hostPath='mongodb+srv://aravindsk:atlaspass@cluster0-msqf4.mongodb.net/test?retryWrites=true'
        self.hostName = '10.0.0.2:27017'
        self.hostPath = 'mongodb://'+self.hostName+'/'
        self.dbName='news_articles'
