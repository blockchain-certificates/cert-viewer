import gridfs
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient(host='mongodb://localhost:27017')
    fs = gridfs.GridFS(client.admin)
    with open('68656c6c6f636f6d7077ffff.json') as infile:
        content = infile.read()
        fs.put(content, filename='68656c6c6f636f6d7077ffff.json', encoding='utf-8')
        #out = fs.find_one({'filename': '68656c6c6f636f6d7077ffff.json'})
        #print (out.read())

