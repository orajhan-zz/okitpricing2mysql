import pymysql
from app import app
from mysql_config import mysql
from flask import jsonify
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash

#GET all prices
@app.route('/ociprice/')
def ociprice():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM ociprice")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

# GET price
#@app.route('/ociprice/<int:sku>')
@app.route('/ociprice/<sku>')
def getprice(sku):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("select * from ociprice where PARTNUMBER=%s", sku)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()

# POST new sku and price
@app.route('/add', methods=['POST'])
def add_sku():
	try:
		json = request.json
		PARTNUMBER = json['PARTNUMBER']
		CURRENCYCODE = json['CURRENCYCODE']
		DISPLAYNAME = json['DISPLAYNAME']
		METRICDISPLAYNAME = json['METRICDISPLAYNAME']
		PAY_AS_YOU_GO = json['PAY_AS_YOU_GO']
		MONTHLY_COMMIT = json['MONTHLY_COMMIT']
		# validate the received values
		if PARTNUMBER and CURRENCYCODE and DISPLAYNAME and METRICDISPLAYNAME and PAY_AS_YOU_GO and MONTHLY_COMMIT and request.method == 'POST':
			#do not save password as a plain text
			#_hashed_password = generate_password_hash(_password)
			#data = (_name, _email, _hashed_password,)
			# save edits
			sql = "INSERT INTO ociprice (PARTNUMBER, CURRENCYCODE, DISPLAYNAME, METRICDISPLAYNAME, PAY_AS_YOU_GO, MONTHLY_COMMIT) values (%s, %s, %s, %s, %s, %s)"
			data = (PARTNUMBER, CURRENCYCODE, DISPLAYNAME, METRICDISPLAYNAME, PAY_AS_YOU_GO, MONTHLY_COMMIT)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('new SKU has been added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run()

