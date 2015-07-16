import os
import json
import hashlib

from app import JSONS_PATH, DATA_PATH, HASHMAP_PATH

hash_mappings = {}
for filename in os.listdir(JSONS_PATH):
	if filename.split(".")[1]=="json":
		raw_data = open(JSONS_PATH+filename).read()
		hex_dig = hashlib.sha256(raw_data).hexdigest()
		hash_mappings[hex_dig]=filename.split(".")[0]

open(HASHMAP_PATH, "wb").write(json.dumps(hash_mappings))