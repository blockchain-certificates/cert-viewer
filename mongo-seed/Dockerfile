FROM mongo

COPY dump /dump
CMD mongorestore --host mongodb --db test /dump/test

# Note: the recipient and certificate files are currently here for reference only. Because we're storing the
# certificates in gridfs, we need to use mongodump and mongorestore to load sample data.
# For reference, this is how it would be done using mongoexport/mongoimport:
# reference: http://stackoverflow.com/questions/31210973/how-do-i-seed-a-mongo-database-using-docker-compose
# example:
# COPY certificates.json /certificates.json
# CMD mongoimport --db test --collection certificates --type json --file certificates.json --jsonArray

# dump db:
# mongodump --db test --out dump