import glob

import gridfs
from pymongo import MongoClient
import os


def load_gridfs(mongodb_uri, cert_dir):
    client = MongoClient(host=mongodb_uri)
    conn = client[mongodb_uri[mongodb_uri.rfind('/') + 1:len(mongodb_uri)]]

    fs = gridfs.GridFS(conn)

    cert_glob = os.path.join(cert_dir, '*.json')
    json_files = glob.glob(cert_glob)

    for f in json_files:
        with open(f) as infile:
            filename = os.path.basename(f)
            content = infile.read()
            fs.put(content, filename=filename, encoding='utf-8')
            out = fs.find_one({'filename': filename})
            print('filename: ' + filename)
            print(out.read())


if __name__ == "__main__":
    mongodb_uri = 'mongodb://localhost:27017/test'
    cert_dir = '.'
    load_gridfs(mongodb_uri, cert_dir)
