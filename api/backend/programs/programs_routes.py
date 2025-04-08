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
# Create a program
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

#------------------------------------------------------------
# Search for all programs 
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
# Get a specific program
@programs.route('/<string:program_id>', methods=['GET'])
def get_program(program_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Programs WHERE program_id = %s', (program_id,))
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchone()
    if result:
        return jsonify(dict(zip(row_headers, result)))
    return jsonify({"error": "Program not found"}), 404

#------------------------------------------------------------
# Get all applications for a specific program
@programs.route('/<string:program_id>/applications', methods=['GET'])
def get_program(program_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Programs WHERE program_id = %s', (program_id,))
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchone()
    if result:
        return jsonify(dict(zip(row_headers, result)))
    return jsonify({"error": "Program not found"}), 404

#------------------------------------------------------------
# Get all user profiles of people who apply for a specific program
@programs.route('/<string:program_id>/profiles', methods=['GET'])
def get_program(program_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Programs WHERE program_id = %s', (program_id,))
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchone()
    if result:
        return jsonify(dict(zip(row_headers, result)))
    return jsonify({"error": "Program not found"}), 404

#------------------------------------------------------------
# Get all feedback forms for a program
@programs.route('/<string:program_id>/feedbacks', methods=['GET'])
def get_program(program_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Programs WHERE program_id = %s', (program_id,))
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchone()
    if result:
        return jsonify(dict(zip(row_headers, result)))
    return jsonify({"error": "Program not found"}), 404

#------------------------------------------------------------
# Get all feedback forms for a program
@programs.route('/programs/ratings', methods=['GET'])
def get_program(program_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Programs WHERE program_id = %s', (program_id,))
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchone()
    if result:
        return jsonify(dict(zip(row_headers, result)))
    return jsonify({"error": "Program not found"}), 404

#------------------------------------------------------------
# Get all feedback forms for a program
@programs.route('/programs/:id/retentions', methods=['GET'])
def get_program(program_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Programs WHERE program_id = %s', (program_id,))
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchone()
    if result:
        return jsonify(dict(zip(row_headers, result)))
    return jsonify({"error": "Program not found"}), 404

#------------------------------------------------------------
# Get all feedback forms for a program
@programs.route('/programs/:id/ratings', methods=['GET'])
def get_program(program_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Programs WHERE program_id = %s', (program_id,))
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchone()
    if result:
        return jsonify(dict(zip(row_headers, result)))
    return jsonify({"error": "Program not found"}), 404

#------------------------------------------------------------
# Update a specific program
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

#------------------------------------------------------------
# Delete a specific program
@programs.route('/<int:program_id>', methods=['DELETE'])
def delete_program(program_id):
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM Programs WHERE program_id = %s', (program_id,))
        db.get_db().commit()
        return jsonify({"message": "Program deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400