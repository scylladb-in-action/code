# Import Flask into your application
from flask import Flask

# Create a Flask app based on the name of the file 
app = Flask(__name__)

# Route HTTP requests to '/' to this function
@app.route('/') 
def hello_world(): 
    # Return the name of the book
    # Flask automatically converts the value into an HTTP response
    return 'ScyllaDB in Action!' 