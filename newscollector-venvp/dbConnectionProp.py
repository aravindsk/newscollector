class dbConnection(object):
    def __init__(self):
        # self.hostPath='mongodb+srv://aravindsk:atlaspass@cluster0-msqf4.mongodb.net/test?retryWrites=true'
        self.hostPath = 'mongodb://10.0.0.2:27017/'
        self.dbName='news_articles'
