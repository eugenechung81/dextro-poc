# REST SERVER
from flask import Flask, jsonify, request
import queryapi

app = Flask(__name__)

# @app.route('/')
# def index():
#     return "Hello, World!"

# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web',
#         'done': False
#     }
# ]

# print queryapi.metas

@app.route('/api/metas', methods=['GET'])
def get_metas():
    return jsonify({'metas': queryapi.metas})

@app.route('/api/keywords/search', methods=['GET'])
def get_keyword_search():
    query = request.args.get('query', '')
    results = queryapi.search_keywords(query)
    return jsonify({'metas': results})

@app.route('/api/counters', methods=['GET'])
def get_counters():
    results = queryapi.get_counters()
    return jsonify({'counters': results})

if __name__ == '__main__':
    app.run(debug=True)