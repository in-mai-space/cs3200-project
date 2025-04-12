###
# Main application interface
###

# import the create app function 
# that lives in src/__init__.py
from backend.app import create_app

# create the app object
app = create_app()

if __name__ == '__main__':
    # we want to run in debug mode (for hot reloading) 
    # this app will be bound to port 4000. 
    # Take a look at the docker-compose.yml to see 
    # what port this might be mapped to... 
    app.run(debug = True, host = '0.0.0.0', port = 4000)


from backend.feedbacks import controllers as feedback_routes
app.register_blueprint(feedback_routes.feedbacks)

from backend.feedbacks import controllers as feedback_routes
app.register_blueprint(feedback_routes.feedbacks)
