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
organizations = Blueprint('organizations', __name__)

#------------------------------------------------------------
# Get all customers from the system
@organizations.route('/', methods=['GET'])
def get_organizations():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Organizations')
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)

#------------------------------------------------------------
# Get customer detail for customer with particular userID
#   Notice the manner of constructing the query. 
@organizations.route('/<int:org_id>', methods=['GET'])
def get_organization(org_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Organizations WHERE org_id = %s', (org_id,))
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchone()
    if result:
        return jsonify(dict(zip(row_headers, result)))
    return jsonify({"error": "Organization not found"}), 404

#------------------------------------------------------------
# Update customer info for customer with particular userID
#   Notice the manner of constructing the query.
@organizations.route('/', methods=['POST'])
def create_organization():
    data = request.json
    cursor = db.get_db().cursor()
    try:
        cursor.execute(
            'INSERT INTO Organizations (name, description, contact_email) VALUES (%s, %s, %s)',
            (data['name'], data.get('description'), data['contact_email'])
        )
        db.get_db().commit()
        return jsonify({"message": "Organization created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@organizations.route('/<int:org_id>', methods=['PUT'])
def update_organization(org_id):
    data = request.json
    cursor = db.get_db().cursor()
    try:
        update_fields = []
        values = []
        for key in ['name', 'description', 'contact_email']:
            if key in data:
                update_fields.append(f"{key} = %s")
                values.append(data[key])
        if not update_fields:
            return jsonify({"error": "No fields to update"}), 400
        values.append(org_id)
        query = f"UPDATE Organizations SET {', '.join(update_fields)} WHERE org_id = %s"
        cursor.execute(query, values)
        db.get_db().commit()
        return jsonify({"message": "Organization updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@organizations.route('/<int:org_id>', methods=['DELETE'])
def delete_organization(org_id):
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM Organizations WHERE org_id = %s', (org_id,))
        db.get_db().commit()
        return jsonify({"message": "Organization deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#------------------------------------------------------------
# Makes use of the very simple ML model in to predict a value
# and returns it to the user
@organizations.route('/prediction/<var01>/<var02>', methods=['GET'])
def predict_value(var01, var02):
    current_app.logger.info(f'var01 = {var01}')
    current_app.logger.info(f'var02 = {var02}')

    returnVal = predict(var01, var02)
    return_dict = {'result': returnVal}

    the_response = make_response(jsonify(return_dict))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response