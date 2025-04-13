########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.database import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
applications = Blueprint('applications', __name__)


#------------------------------------------------------------
# Get all customers from the system
@applications.route('/applications', methods=['GET'])
def get_applications():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT id, company, last_name,
                    first_name, job_title, business_phone FROM customers
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Update customer info for customer with particular userID
#   Notice the manner of constructing the query.
@applications.route('/applications', methods=['PUT'])
def update_application():
    current_app.logger.info('PUT /applications route')
    application_info = request.json
    application_id = application_info['id']
    name = application_info['name']
    description = application_info['description']
    category = application_info['category']

    query = 'UPDATE applications SET name = %s, description = %s, category = %s where id = %s'
    data = (name, description, category, application_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'application updated!'

#------------------------------------------------------------
# Get customer detail for customer with particular userID
#   Notice the manner of constructing the query. 
@applications.route('/applications/<applicationID>', methods=['GET'])
def get_application(applicationID):
    current_app.logger.info('GET /applications/<applicationID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT id, name, description, category FROM applications WHERE id = {0}'.format(applicationID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Makes use of the very simple ML model in to predict a value
# and returns it to the user
@applications.route('/prediction/<var01>/<var02>', methods=['GET'])
def predict_value(var01, var02):
    current_app.logger.info(f'var01 = {var01}')
    current_app.logger.info(f'var02 = {var02}')

    returnVal = predict(var01, var02)
    return_dict = {'result': returnVal}

    the_response = make_response(jsonify(return_dict))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response