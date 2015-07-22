This is a Dextro POC, attempting to apply computer vision using Alchemy API.  The file is dropped in the import directory and the ingestor will generate meta tags and thumbnails with keywords generating off of the images.  

To query the image details, there are serveral exposed REST APIs -- getting all meta tags, querying based on keyword and getting count of keywords.

### To run ingestor:

$ python ingestor.py

Outputs thumbnails to "export/" directory and generates metas.json

### To run rest services:

$ sudo python server.py

Reads from metas.json and runs flask rest server.

http://localhost:5000/api/metas
http://localhost:5000/api/keywords/search?query=food
http://localhost:5000/api/counters

## Thumbnail Extraction

These thumbnails are automatically produced by the ingestor which in turn is sent to Alchemy API to extract out the image tags. 

![alt text](https://raw.githubusercontent.com/eugenechung81/dextro-poc/master/guide/movie-banana-2.png "Image")

![alt text](https://raw.githubusercontent.com/eugenechung81/dextro-poc/master/guide/movie-banana-4.png "Image")

## Sample Queries 

Sample queries on the ingested sample videos.  

![alt text](https://raw.githubusercontent.com/eugenechung81/dextro-poc/master/guide/counter.png "Image")

![alt text](https://raw.githubusercontent.com/eugenechung81/dextro-poc/master/guide/search.png "Image")
