# from lxml.objectify import deannotate
# from analyzer import VideoDescriptor

__author__ = 'eugene'

class VideoMeta(object):
    def __init__(self, descriptor, keywords, video_location, thumbnails):
        self.descriptor = descriptor
        self.keywords = keywords
        self.video_location = video_location
        self.thumbnails = thumbnails
    def __str__(self):
        return str(self.__dict__) # shows inner map
    def __repr__(self):
        return str(self.__dict__) # shows inner map
# keywords = {}
# keywords['food'] = 0.354344
# descriptor = VideoDescriptor(5.83,5379338,"128x72","RGB")
# metas = []
# meta = VideoMeta(descriptor, keywords, "", [])
# metas.append(meta)

class VideoDescriptor(object):
    def __init__(self, duration, bit_rate, frame_size, frame_mode):
        self.duration = duration
        self.bit_rate = bit_rate
        self.frame_size = frame_size
        self.frame_mode = frame_mode
    def __str__(self):
        return str(self.__dict__) # shows inner map
    def __repr__(self):
        return str(self.__dict__) # shows inner map

        # print(json.dumps(test, indent=4)) # doesn't work
        # from pprint import pprint
        # pprint (vars(test))

# TODO Later
# class MetaGenerator(object):
#     # @staticmethod
#     # def generate(video_file):
#     # MetaGenerator.generate('banana-test.mp4')
#     def generate(self,video_file):
#         """
#
#         :param video_file:
#         :return meta
#         """
#         pass
# meta_gen = MetaGenerator()
# meta = meta_gen.generate('banana-test.mp4')
# metas = generate_metas()

def print_json(obj):
    import json
    # print(json.dumps(meta, indent=4))
    # TypeError: {'keywords': {'food': 0.354344}, 'descriptor': {'duration': 5.83, 'bit_rate': 5379338, 'frame_mode': 'RGB', 'frame_size': '128x72'}} is not JSON serializable
    # print(json.dumps(meta.__dict__))
    print(json.dumps(obj, default=lambda o: o.__dict__, indent=4))

def write_json(obj, file):
    import json
    with open(file, 'w') as outfile:
        json.dump(obj, outfile, default=lambda o: o.__dict__, indent=4)
    print 'Written json to: ' + file

def read_json(file):
    obj = None
    import json
    with open(file) as json_data:
        obj = json.load(json_data)
        json_data.close()
    print 'Read json: ' + file
    return obj
# write_json(metas, 'metas.txt')
# tests = read_json('metas.txt')
# print_json(tests)

def generate_keywords(image_filename):
    keywords = {}
    from alchemyapi import AlchemyAPI
    import json
    alchemyapi = AlchemyAPI()
    response = alchemyapi.imageTagging('image', image_filename)
    if response['status'] == 'OK':
        #print('## Response Object ##')
        #print(json.dumps(response, indent=4))
        print 'alchmey response: ' + str(response)

        for keyword in response['imageKeywords']:
            keywords[keyword['text']] = keyword['score']
    else:
        print('Error in image tagging call: ', response['statusInfo'])
    return keywords
#keywords = generate_keywords('export/banana-test-4.jpeg')
#keywords = generate_keywords('export/banana-test-2.jpeg')

def generate_descriptor(video_filename):
    from ffvideo import VideoStream
    vs = VideoStream(video_filename, frame_size=(128, None))
    return VideoDescriptor(vs.duration, vs.bitrate, vs.frame_size, vs.frame_mode)

def generate_thumbnails(video_filename):
    thumbnails = []
    from ffvideo import VideoStream
    vs = VideoStream(video_filename, frame_size=(128, None))

    frame = vs.get_frame_at_sec(2)
    thumbnail = 'export/' + video_filename.split(".")[0] + '-2.jpeg'
    frame.image().save(thumbnail)
    print "thumbnail saved: " + thumbnail

    # NoMoreData: Unable to read frame. [-541478725]
    frame = vs.get_frame_at_sec(6)
    thumbnail = 'export/' + video_filename.split(".")[0] + '-4.jpeg'
    frame.image().save(thumbnail)
    print "thumbnail saved: " + thumbnail

    thumbnails.append(thumbnail)
    return thumbnails
# generate_thumbnails('banana-test.mp4')

def get_second_marks(duration):
    import math
    #x = math.ceil(1.9)
    #duration = 20
    #duration = 5.8
    range_list = range(0,int(duration),int(math.ceil(duration/3)))
    # print range_list[0:3]
    return range_list

def generate_meaningful_thumbnails(video_filename):
    """
    Generate around bounds of thumbnails.  e.g. atleast 3 thumbnails within bounds, return as named tuple, see if scene
    has changed.
    :param video_filename:
    """
    # http://stackoverflow.com/questions/354883/how-do-you-return-multiple-values-in-python
    # TODO pass later
    descriptor = generate_descriptor(video_filename)
    thumbnails = []
    second_marks = get_second_marks(descriptor.duration)
    from ffvideo import VideoStream
    vs = VideoStream(video_filename, frame_size=(128, None))
    for sec in second_marks:
        frame = vs.get_frame_at_sec(sec)
        # strip out import
        filename = video_filename.replace("import/", "", 1)
        thumbnail = 'export/' + filename.split(".")[0] + '-' + str(sec) + '.jpeg'
        frame.image().save(thumbnail)
        print "thumbnail saved: " + thumbnail
        thumbnails.append(thumbnail)
    return thumbnails

def generate_all_keywords(thumbnails):
    all_keyswords = {}
    for thumbnail in thumbnails:
        keywords = generate_keywords(thumbnail)
        all_keyswords =  dict(all_keyswords, **keywords)
    # thumbnails = generate_thumbnails(video_filename)
    return all_keyswords

# sample: {'keywords': {u'food': u'0.5'}, 'descriptor': {'duration': 5.833333333333333, 'bit_rate': 5379338, 'frame_mode': 'RGB', 'frame_size': (128, 72)}}
def generate_meta(video_filename):
    print '# generating meta: ' + video_filename
    descriptor = generate_descriptor(video_filename)
    thumbnails = generate_meaningful_thumbnails(video_filename)
    keywords = generate_all_keywords(thumbnails)
    return VideoMeta(descriptor, keywords, video_filename, thumbnails)
# meta = generate_meta('banana-test.mp4')
# meta = generate_meta('import/cartoon-bunny.mp4')
# meta = generate_meta('import/water-leaves.wmv')

def ingest():
    metas = []
    import os
    video_filenames = map(lambda f : 'import/' + f, os.listdir('import'))
    for video_filename in video_filenames:
        # catch exceptions / retry logic later
        metas.append(generate_meta(video_filename))
    print 'Done ingesting'
    write_json(metas, 'metas2.json')

ingest()

