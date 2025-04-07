########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify
from flask import make_response
from flask import current_app
from backend.database import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
programs = Blueprint('programs', __name__)


#------------------------------------------------------------
# Get all customers from the system
@programs.route('/', methods=['GET'])
def get_programs():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Programs')
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)

#------------------------------------------------------------
# Get customer detail for customer with particular userID
#   Notice the manner of constructing the query. 
@programs.route('/<int:program_id>', methods=['GET'])
def get_program(program_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Programs WHERE program_id = %s', (program_id,))
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchone()
    if result:
        return jsonify(dict(zip(row_headers, result)))
    return jsonify({"error": "Program not found"}), 404

#------------------------------------------------------------
# Makes use of the very simple ML model in to predict a value
# and returns it to the user
@programs.route('/prediction/<var01>/<var02>', methods=['GET'])
def predict_value(var01, var02):
    current_app.logger.info(f'var01 = {var01}')
    current_app.logger.info(f'var02 = {var02}')

    returnVal = predict(var01, var02)
    return_dict = {'result': returnVal}

    the_response = make_response(jsonify(return_dict))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@programs.route('/', methods=['POST'])
def create_program():
    data = request.json
    cursor = db.get_db().cursor()
    try:
        cursor.execute(
            'INSERT INTO Programs (name, description, org_id, start_date, end_date) VALUES (%s, %s, %s, %s, %s)',
            (data['name'], data.get('description'), data['org_id'], data.get('start_date'), data.get('end_date'))
        )
        db.get_db().commit()
        return jsonify({"message": "Program created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@programs.route('/<int:program_id>', methods=['PUT'])
def update_program(program_id):
    data = request.json
    cursor = db.get_db().cursor()
    try:
        update_fields = []
        values = []
        for key in ['name', 'description', 'org_id', 'start_date', 'end_date']:
            if key in data:
                update_fields.append(f"{key} = %s")
                values.append(data[key])
        if not update_fields:
            return jsonify({"error": "No fields to update"}), 400
        values.append(program_id)
        query = f"UPDATE Programs SET {', '.join(update_fields)} WHERE program_id = %s"
        cursor.execute(query, values)
        db.get_db().commit()
        return jsonify({"message": "Program updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@programs.route('/<int:program_id>', methods=['DELETE'])
def delete_program(program_id):
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM Programs WHERE program_id = %s', (program_id,))
        db.get_db().commit()
        return jsonify({"message": "Program deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@programs.route('/organization/<int:org_id>', methods=['GET'])
def get_programs_by_organization(org_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Programs WHERE org_id = %s', (org_id,))
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)