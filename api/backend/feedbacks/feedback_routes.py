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
feedbacks = Blueprint('feedbacks', __name__)


#------------------------------------------------------------
# Get all customers from the system
@feedbacks.route('/feedbacks', methods=['GET'])
def get_feedbacks():

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
@feedbacks.route('/feedbacks', methods=['PUT'])
def update_feedback():
    current_app.logger.info('PUT /feedbacks route')
    feedback_info = request.json
    feedback_id = feedback_info['id']
    name = feedback_info['name']
    description = feedback_info['description']
    category = feedback_info['category']

    query = 'UPDATE feedbacks SET name = %s, description = %s, category = %s where id = %s'
    data = (name, description, category, feedback_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'feedback updated!'

#------------------------------------------------------------
# Get customer detail for customer with particular userID
#   Notice the manner of constructing the query. 
@feedbacks.route('/feedbacks/<feedbackID>', methods=['GET'])
def get_feedback(feedbackID):
    current_app.logger.info('GET /feedbacks/<feedbackID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT id, name, description, category FROM feedbacks WHERE id = {0}'.format(feedbackID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Makes use of the very simple ML model in to predict a value
# and returns it to the user
@feedbacks.route('/prediction/<var01>/<var02>', methods=['GET'])
def predict_value(var01, var02):
    current_app.logger.info(f'var01 = {var01}')
    current_app.logger.info(f'var02 = {var02}')

    returnVal = predict(var01, var02)
    return_dict = {'result': returnVal}

    the_response = make_response(jsonify(return_dict))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response