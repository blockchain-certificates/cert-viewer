import gridfs
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient(host='mongodb://localhost:27017')
    fs = gridfs.GridFS(client.test)
    with open('f813349f-1385-487f-8d89-38a092411fa5.json') as infile:
        #content = infile.read()
        #fs.put(content, filename='f813349f-1385-487f-8d89-38a092411fa5.json', encoding='utf-8')
        out = fs.find_one({'filename': 'f813349f-1385-487f-8d89-38a092411fa5.json'})
        print(out.read())

