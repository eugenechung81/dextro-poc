#from analyzer import read_json, print_json

__author__ = 'eugene'

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

###

metas = read_json('metas.json')
# print_json(metas)

# e.g. query='food'
def search_keywords(query):
    filtered_metas = filter(lambda v: query in v['keywords'].keys(), metas)
    # print_json(filtered_metas)
    print 'files: %s' % map(lambda m: m['video_location'], filtered_metas)
    print '# of results: %d' % len(filtered_metas)
    return filtered_metas
# search_keywords('food')

def get_counters():
    list = map(lambda m: m['keywords'].keys(), metas)
    flattened = [val for sublist in list for val in sublist]
    from collections import Counter
    counters = Counter(flattened)
    print_json(counters)
    return counters
# get_counters()

