README.txt

This is a Dextro POC, attempting to apply computer vision using Alchemy API.  The file is dropped in the import directory and the ingestor will generate meta tags and thumbnails with keywords generating off of the images.  

TO query the image details, there are serveral exposed REST APIs -- getting all meta tags, querying based on keyword and getting count of keywords.

###

To run ingestor:

$ python ingestor.py

Outputs thumbnails to "export/" directory and generates metas.json

###

To run rest services:

$ sudo python server.py

Reads from metas.json and runs flask rest server.

http://localhost:5000/api/metas
http://localhost:5000/api/keywords/search?query=food
http://localhost:5000/api/counters
