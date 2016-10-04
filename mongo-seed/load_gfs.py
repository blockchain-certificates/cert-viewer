import gridfs
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient(host='mongodb://localhost:27017')
    fs = gridfs.GridFS(client.test)
    files = ['f813349f-1385-487f-8d89-38a092411fa5.json', 'b5dee02e-50cd-4e48-ad33-de7d2eafa359.json']
    for f in files:
        with open(f) as infile:
            content = infile.read()
            fs.put(content, filename=f, encoding='utf-8')
            out = fs.find_one({'filename': f})
            print(out.read())