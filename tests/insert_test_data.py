

from certificates.certificate_repo import UserData
import certificates.config

import gridfs
from certificates import ui_helpers
from pymongo import MongoClient

client = MongoClient(host=secrets.MONGO_URI)

gfs = gridfs.GridFS(client['admin'])
service = Service(client, gfs)

if __name__ == '__main__':
    user_data = UserData('K3', 'r@r.com', 'a.b.s', 'some comments', 'satoshi', 'nakamoto', '111 main st',
                         'seattle', 'wa', '96666', 'usa')
    service.certificate_repo.create_user(user_data)
    cert_json = {}
    cert_json['pubkey'] = 'K3'
    cert_json['issued'] = True
    cert_json['txid'] = 't1'
    cert_id = service.certificate_repo.insert_certificate(cert_json)
    file_name = str(cert_id.inserted_id) + '.json'
    data = config.read_file('66a00099a2b165359bd9ac2c.json')

    gfs.put(data, filename=file_name, encoding='UTF-8')

    f1 = gfs.find_one({'filename': file_name})
    print(f1)


    #t1 = service.certificates.client.admin.certificates.find()
    #[print(str(t['_id'])) for t in t1]
    #t2 = service.certificates.client.admin.recipients.find()
    #t1 = service.get_formatted_certificate('572d4186faf890490e33df15', None)
    #print(t1)
