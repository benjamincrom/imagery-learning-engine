import datetime

from flask import Flask, request
from flask_restful import reqparse, Api, Resource
from pymongo import MongoClient


app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

client = MongoClient('localhost', 27017)
imagery_database = client.imagery_database
annotation_table = imagery_database.annotation_table


class CreateImage(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        annotation_data = {
            'x': float(json_data['x']),
            'y': float(json_data['y']),
            'width': float(json_data['width']),
            'height': float(json_data['height']),
            'text': json_data['text'],
            'filename': json_data['filename'],
            'created_datetime': datetime.datetime.utcnow()
        }

        result = annotation_table.insert_one(annotation_data)
        return {'Annotation_ID': '{0}'.format(result.inserted_id)}


class UpdateImage(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        filter_data = {
            'x': float(json_data['x']),
            'y': float(json_data['y']),
            'width': float(json_data['width']),
            'height': float(json_data['height']),
            'filename': json_data['filename']
        }

        annotation_data = {
            'x': float(json_data['x']),
            'y': float(json_data['y']),
            'width': float(json_data['width']),
            'height': float(json_data['height']),
            'text': json_data['text'],
            'filename': json_data['filename'],
            'created_datetime': datetime.datetime.utcnow()
        }

        result = annotation_table.update_one(filter_data, annotation_data)
        return {'Annotation_ID': '{0}'.format(result.inserted_id)}


class DeleteImage(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        annotation_data = {
            'x': float(json_data['x']),
            'y': float(json_data['y']),
            'width': float(json_data['width']),
            'height': float(json_data['height']),
            'text': json_data['text'],
            'filename': json_data['filename'],
        }

        result = annotation_table.delete_one(annotation_data)
        return {'Annotation_ID': '{0}'.format(result.inserted_id)}


api.add_resource(CreateImage, '/api/annotation')
api.add_resource(UpdateImage, '/api/update_annotation')
api.add_resource(DeleteImage, '/api/delete_annotation')

if __name__ == '__main__':
    app.run(debug=True)

#bills_post = imagery_database.find_one({'author': 'Bill'})
#print(bills_post)
