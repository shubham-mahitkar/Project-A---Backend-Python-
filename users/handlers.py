from users.app import app
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin
from users.models.sql.query import UserModel
from users.models.neo4j.cypher import CypherModel
from users.connectors.neo4j import drive
import json

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

		if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			user = UserModel()
			data = user.add_user(_name, _email, _hashed_password)
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
		neo_user = CypherModel()
		rows = neo_user.user_details_by_id(id)
		print("rows: ", rows)
		inner_obj = {}
		inner_obj['id']= row[0]
		inner_obj['name']= row[1]
		inner_obj['email']= row[2]
		inner_obj['password']= row[3]
		# lst.append(inner_obj)
		inner_obj['application'] = rows['application']
		return inner_obj
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
		if _name and _email and _id and request.method == 'PUT':
			user = UserModel()
			data = user.update_user(_name, _email, id)
			resp = jsonify(data)
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
		return e
		
@app.route('/delete/<int:id>', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def delete_user(id):
	try:
		user = UserModel()
		user.delete_user(id)
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
        print("ress: ", rows)
        return rows
    except Exception as e:
        print(e)