########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify
from flask import make_response
from flask import current_app
from backend.database import db
from backend.utils.query_validation import (
    validate_query_params,
    validate_category_param
)

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
users = Blueprint('users', __name__)

# Define allowed query parameters
ALLOWED_QUERY_PARAMS = [
    'role',  # Example category from database
    'status',
    'created_after',
    'created_before',
    'limit',
    'offset'
]

#------------------------------------------------------------
# Get all customers from the system
@users.route('/', methods=['GET'])
def get_users():
    # Validate query parameters
    validation_error = validate_query_params(
        request.args,
        ALLOWED_QUERY_PARAMS,
        'Users'  # Table name for schema validation
    )
    if validation_error:
        return validation_error
    
    # Validate role category if provided
    if 'role' in request.args:
        validation_error = validate_category_param(
            request.args,
            'role',
            'Users',
            'role'  # Column name containing roles
        )
        if validation_error:
            return validation_error
    
    # Build query based on validated parameters
    cursor = db.get_db().cursor()
    query = 'SELECT * FROM Users WHERE 1=1'
    params = []
    
    if 'role' in request.args:
        query += ' AND role = %s'
        params.append(request.args['role'])
    
    if 'status' in request.args:
        query += ' AND status = %s'
        params.append(request.args['status'])
    
    if 'created_after' in request.args:
        query += ' AND created_at >= %s'
        params.append(request.args['created_after'])
    
    if 'created_before' in request.args:
        query += ' AND created_at <= %s'
        params.append(request.args['created_before'])
    
    # Add pagination
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    query += ' LIMIT %s OFFSET %s'
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)

#------------------------------------------------------------
# Get customer detail for customer with particular userID
#   Notice the manner of constructing the query. 
@users.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Users WHERE user_id = %s', (user_id,))
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchone()
    if result:
        return jsonify(dict(zip(row_headers, result)))
    return jsonify({"error": "User not found"}), 404

#------------------------------------------------------------
# Makes use of the very simple ML model in to predict a value
# and returns it to the user
@users.route('/prediction/<var01>/<var02>', methods=['GET'])
def predict_value(var01, var02):
    current_app.logger.info(f'var01 = {var01}')
    current_app.logger.info(f'var02 = {var02}')

    returnVal = predict(var01, var02)
    return_dict = {'result': returnVal}

    the_response = make_response(jsonify(return_dict))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@users.route('/', methods=['POST'])
def create_user():
    data = request.json
    cursor = db.get_db().cursor()
    try:
        cursor.execute(
            'INSERT INTO Users (email, password, first_name, last_name, phone, date_of_birth) VALUES (%s, %s, %s, %s, %s, %s)',
            (data['email'], data['password'], data['first_name'], data['last_name'], 
             data.get('phone'), data.get('date_of_birth'))
        )
        db.get_db().commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@users.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    cursor = db.get_db().cursor()
    try:
        update_fields = []
        values = []
        for key in ['email', 'password', 'first_name', 'last_name', 'phone', 'date_of_birth']:
            if key in data:
                update_fields.append(f"{key} = %s")
                values.append(data[key])
        if not update_fields:
            return jsonify({"error": "No fields to update"}), 400
        values.append(user_id)
        query = f"UPDATE Users SET {', '.join(update_fields)} WHERE user_id = %s"
        cursor.execute(query, values)
        db.get_db().commit()
        return jsonify({"message": "User updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@users.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM Users WHERE user_id = %s', (user_id,))
        db.get_db().commit()
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400