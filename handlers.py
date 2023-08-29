import pymysql
from users.app import app
from users.connectors.db import mysql
from flask import Flask, request, jsonify
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin
import json


@app.route('/add', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_user():
	cursor = None
	try:
		_json = request.json
		if "name" in _json:
			_name = _json['name']
		else:
			print("missing field 'name'")
			_name = "empty"
		if "email" in _json:
			_email = _json['email']
		else:
			print("missing field 'email'")
			_email = "empty"
		if "password" in _json:
			_password = _json['password']
		else:
			print("missing field 'password'")
			_password = "empty"

		if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
			data = (_name, _email, _hashed_password,)
			cursor = mysql.connection.cursor()
			cursor.execute(sql, data)
			mysql.connection.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 


@app.route('/users')
@cross_origin(supports_credentials=True)
def users():
	cursor = None
	lst = []
	count = 0
	try:
		cursor = mysql.connection.cursor()
		cursor.execute("SELECT user_id id, user_name name, user_email email, user_password password FROM tbl_user")
		rows = cursor.fetchall()
		for x in rows:
			inner_obj = {}
			inner_obj['id']= x[0]
			inner_obj['name']= x[1]
			inner_obj['email']= x[2]
			inner_obj['password']= x[3]
			lst.insert(count+1, inner_obj)
			count+=1
		return lst
	except Exception as e:
		print(e)
	finally:
		cursor.close() 


@app.route('/user/<int:id>')
@cross_origin(supports_credentials=True)
def user(id):
	cursor = None
	lst=[]
	try:
		cursor = mysql.connection.cursor()
		cursor.execute(f"SELECT user_id id, user_name name, user_email email, user_password password FROM tbl_user WHERE user_id={id}")
		row = cursor.fetchone()
		inner_obj = {}
		inner_obj['id']= row[0]
		inner_obj['name']= row[1]
		inner_obj['email']= row[2]
		inner_obj['password']= row[3]
		lst.append(inner_obj)
		return lst
	except Exception as e:
		print(e)
	finally:
		cursor.close() 

@app.route('/update', methods=['PUT'])
@cross_origin(supports_credentials=True)
def update_user():
	cursor = None
	try:
		_json = request.json
		if "id" in _json:
			_id = _json['id']
		else:
			print("missing field 'id'")
			return not_found()
		if "name" in _json:
			_name = _json['name']
		else:
			print("missing field 'name'")
			_name = "empty"
		if "email" in _json:
			_email = _json['email']
		else:
			print("missing field 'email'")
			_email = "empty"
		if "password" in _json:
			_password = _json['password']
		else:
			print("missing field 'password'")
			_password = "empty"

		if _name and _email and _password and _id and request.method == 'PUT':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			sql = "UPDATE tbl_user SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
			data = (_name, _email, _hashed_password, _id,)
			cursor = mysql.connection.cursor()
			cursor.execute(sql, data)
			mysql.connection.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
		return e
	finally:
		cursor.close() 
		
@app.route('/delete/<int:id>', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def delete_user(id):
	cursor = None
	try:
		cursor = mysql.connection.cursor()
		cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
		mysql.connection.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		
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


# if __name__ == "__main__":
#     app.run(debug=True)
