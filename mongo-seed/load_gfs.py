import gridfs
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient(host='mongodb://localhost:27017')
    fs = gridfs.GridFS(client.admin)
    with open('573bae27faf890c4d9efcf23.json') as infile:
        content = infile.read()
        #fs.put(content, filename='573bae27faf890c4d9efcf23.json', encoding='utf-8')
        out = fs.find_one({'filename': '573bae27faf890c4d9efcf23.json'})
        print (out.read())

