import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
import json
import requests


def calculateBAC(alcoholConsumed, bodyWeight, gender, time):
    gender.lower()
    '''
    CAS = {[alcohol consumido en gramos / (peso corporal en gramos x r)] x 100} - (0.015 * tiempo transcurrido del ultimo trago en horas)
    '''
    # Converting bodyweight from lbs to grams.
    bodyWeight = bodyWeight * 453.592

    if gender == 'm':
        r = 0.68
        bloodAlcohol = (((alcoholConsumed /
                          (bodyWeight * r)) * 100) - (0.015 * time))
        return bloodAlcohol
    elif gender == 'f':
        r = 0.55
        bloodAlcohol = (((alcoholConsumed /
                          (bodyWeight * r)) * 100) - (0.015 * time))
        return bloodAlcohol
    else:
        return 0


# Calculate Net Alcohol Consumed in Grams.
def getAlcoholConsumed(alcoholPercent, volume):
    grossAlcohol = (alcoholPercent / 100) * volume
    netAlcohol = grossAlcohol * 0.8
    return netAlcohol


@app.route('/add', methods=['POST'])
def add_drink():
    try:
        _json = request.json
        _name = _json['name']
        _volume = _json['volume']
        _alclevel = _json['alclevel']
        if _name and _volume and _alclevel and request.method == 'POST':
            # save edits
            sql = "INSERT INTO tbl_Drinks(drink_name, drink_volume, drink_alclevel) VALUES(%s, %s, %s)"
            data = (_name, _volume, _alclevel,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Drink added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/drinks')
def drinks():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM tbl_Drinks")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/calculateBAC')
def getBAC():
    drinkId = request.args.get('drinkId')
    weight = request.args.get('weight')
    gender = request.args.get('gender')
    time = request.args.get('time')
    r = requests.get('http://localhost:5000/drinks/' + drinkId)
    response = r.json()
    alcoholPercent = response['drink_alclevel']
    volume = response['drink_volume']
    alcoholConsumed = getAlcoholConsumed(alcoholPercent, volume)
    bloodAlcoholContent = calculateBAC(
        alcoholConsumed, float(weight), gender, float(time))
    resp = jsonify(str(bloodAlcoholContent.__round__(2)))
    resp.status_code = 200
    return resp


@app.route('/drinks/<int:id>')
def drink(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT drink_id, drink_name, drink_volume, drink_alclevel FROM tbl_Drinks WHERE drink_id=%s", id)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update', methods=['POST'])
def update_drink():
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _volume = _json['volume']
        _alclevel = _json['alclevel']
        if _name and _volume and _alclevel and request.method == 'POST':
            sql = "UPDATE tbl_Drinks SET drink_name=%s, drink_volume=%s, drink_alclevel=%s WHERE drink_id=%s"
            data = (_name, _volume, _alclevel, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Drink updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete/<int:id>')
def delete_drink(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbl_Drinks WHERE drink_id=%s", (id,))
        conn.commit()
        resp = jsonify('Drink deleted successfully!')
        resp.status_code = 200
        return resp
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
