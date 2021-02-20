from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://exceed_user:1q2w3e4r@158.108.182.0:4321/exceed_backend'
mongo = PyMongo(app)

myCollection = mongo.db.g15

# @app.route('/update', methods=['PATCH'])
# def update():
#     data = request.json

#     filt = { : }
#     updated_content = {"$set": {'slot1' : data["content1"]},
#                                 {'time1'},
#                                 {'cost1'},
#                                 {'slot2'},
#                                 {'time2'}
#                                 {'cost2'},
#                                 {'slot3'},
#                                 {'slot4'}
#                                 {'time1'}
#                                 {'cost1'},
#                                 {'slot4'}
#                                 {'slot4'}
#                                 {'slot4'}
#                                 {'slot4'}
#                                 {'slot4'}
#                                 {'slot4'}}

#     myCollection.update_one(filt, updated_content)

#     return {'result' : 'Updated successfully'}
