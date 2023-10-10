from users.app import app
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin
from users.models.sql.query import UserModel
from users.models.neo4j.cypher import CypherModel
from users.models.snowflake.snowflake_sql import SnowflakeModel
from users.connectors.neo4j import drive
import json
import csv
import io

@app.route('/add', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_user():
	try:
		_json = request.json
		if "name" in _json:
			_name = _json['name']
		else:
			raise Exception("Missing field 'name'")
		if "email" in _json:
			_email = _json['email']
		else:
			raise Exception("Missing field 'email'")
		if "password" in _json:
			_password = _json['password']
		else:
			raise Exception("Missing field 'password'")
		if "application" in _json:
			_application = _json['application']
		else:
			raise Exception("Application is not registerd")

		if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			user = UserModel()
			data = user.add_user(_name, _email, _hashed_password)
			id = data['id']
			neo_user = CypherModel()
			apps = neo_user.add_user_application(id, _name, _application)
			data["application"] = apps
			resp = jsonify(data)
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)


@app.route('/users')
@cross_origin(supports_credentials=True)
def users():
	try:
		user = UserModel()
		rows = user.get_users()
		neo_user = CypherModel()
		neo_rows = neo_user.get_users_applications_from_neo4j()
		for id in rows:
			app_list = []
			for neoid in neo_rows:
				if id['id'] != neoid['neo_id']:
					continue
				else:
					app_list.append(neoid['application'])
					id['application'] = app_list
		return jsonify(rows)
	except Exception as e:
		print(e)


@app.route('/user/<int:id>')
@cross_origin(supports_credentials=True)
def user(id):
	lst=[]
	try:
		user = UserModel()
		row = user.user_details(id)
		if row is None:
			raise Exception("ID Not Found")
		inner_obj = {}
		inner_obj['id']= row[0]
		inner_obj['name']= row[1]
		inner_obj['email']= row[2]
		inner_obj['password']= row[3]
		neo_user = CypherModel()
		rows = neo_user.user_details_by_id(id)
		if rows == None:
			lst.append(inner_obj)
			return jsonify(lst)
		elif row[0] == rows['neo_id']:
			inner_obj['application'] = rows['application']
		else:
			inner_obj['application'] = ['no application registerd']
		snowflake = SnowflakeModel()
		followers, labels = snowflake.get_followers_by_user(inner_obj['name'])
		if followers or labels:
			inner_obj['followers'] = int(followers[0])
			inner_obj['labels'] = labels
		lst.append(inner_obj)
		return jsonify(lst)
	except Exception as e:
		print(e)

@app.route('/user/<int:id>/awards')
@cross_origin(supports_credentials=True)
def awards(id):
	try:
		lst = []
		snowflake = SnowflakeModel()
		awards = snowflake.get_awards_by_id(id)
		for row in awards:
			lst.append(row)
		return jsonify(lst)
	except Exception as e:
		print(e)

@app.route('/update/<int:id>', methods=['PUT'])
@cross_origin(supports_credentials=True)
def update_user(id):
	try:
		_json = request.json
		if "id" in _json:
			_id = _json['id']
		else:
			raise Exception("ID Not Found")
		if "name" in _json:
			_name = _json['name']
		else:
			raise Exception("Missing field 'name'")
		if "email" in _json:
			_email = _json['email']
		else:
			raise Exception("Missing field 'email'")
		if "application" in _json:
			_application = _json['application']
		else:
			raise Exception("Application is not registerd")
		if _name and _email and _id and request.method == 'PUT':
			user = UserModel()
			data = user.update_user(_name, _email, id)
			neo_user = CypherModel()
			apps = neo_user.update_user_applications_by_id(_name, id, _application)
			data["application"] = apps
			resp = jsonify(data)
			resp.status_code = 200
			return resp
	except Exception as e:
		print(e)
		return e
		
@app.route('/delete/<int:id>', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def delete_user(id):
	try:
		user = UserModel()
		user.delete_user(id)
		neo_user = CypherModel()
		neo_user.delete_user_application(id)
		resp = jsonify({"result":'User deleted successfully!'})
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)


@app.errorhandler(404)
@cross_origin(supports_credentials=True)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/neo4j')
@cross_origin(supports_credentials=True)
def get_users_applications():
    try:
        user = CypherModel()
        rows = user.get_users_applications_from_neo4j()
        return rows
    except Exception as e:
        print(e)

@app.route('/neo4j/<int:id>')
@cross_origin(supports_credentials=True)
def get_users_applications_by_id(id):
    try:
        user = CypherModel()
        rows = user.user_details_by_id(id)
        return rows
    except Exception as e:
        print(e)

@app.route('/bulk-user', methods=['POST'])
def bulk_user_upload():
    try:
        csv_file = request.files['file']
        insert_bulk_users(csv_file)
        return jsonify({"message": "Bulk user upload successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def insert_bulk_users(csv_file):
    csv_data = io.StringIO(csv_file.read().decode('utf-8'))
    data = csv.reader(csv_data)

    snowflake = SnowflakeModel()
    snowflake.snowflake_insert_bulk_users(data)
    csv_data.seek(0)

    user = UserModel()
    user.mysql_insert_bulk_users(data)
    csv_data.seek(0)

    neo = CypherModel()
    neo.neo4j_insert_bulk_users(data)
