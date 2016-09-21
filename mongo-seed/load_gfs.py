import gridfs
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient(host='mongodb://localhost:27017')
    fs = gridfs.GridFS(client.test)
    with open('4119a68e-e31a-4508-8b07-3bf9ab968089.json') as infile:
        content = infile.read()
        fs.put(content, filename='4119a68e-e31a-4508-8b07-3bf9ab968089.json', encoding='utf-8')
        out = fs.find_one({'filename': '4119a68e-e31a-4508-8b07-3bf9ab968089.json'})
        print(out.read())

