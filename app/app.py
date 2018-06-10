import datetime
import os

from flask import Flask, request, render_template
from flask_restful import reqparse, Api, Resource
from pymongo import MongoClient


app = Flask(__name__, static_url_path='')
api = Api(app)
parser = reqparse.RequestParser()

client = MongoClient('localhost', 27017)
imagery_database = client.imagery_database
annotation_table = imagery_database.annotation_table


class UpsertImage(Resource):
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
            'modified_datetime': datetime.datetime.utcnow()
        }

        result = annotation_table.update(filter_data, annotation_data, True)
        return {'modified_count': '{}'.format(result['n'])}


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

        result = annotation_table.delete_many(annotation_data)
        return {'deleted_count': '{0}'.format(result.deleted_count)}


api.add_resource(UpsertImage, '/api/annotation')
api.add_resource(DeleteImage, '/api/delete_annotation')

@app.route('/')
def root():
    filename_list = os.listdir('app/static/img')
    annotation_list = [entry for entry in annotation_table.find()]
    return render_template('index.html',
                           filename_list=filename_list,
                           annotation_list=annotation_list)

if __name__ == '__main__':
    app.run(debug=True)
