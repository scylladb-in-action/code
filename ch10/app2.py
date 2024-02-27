# Import the cluster from the Scylla driver (which uses the Cassandra API)
from cassandra.cluster import Cluster

# Import the Flask global context
from flask import Flask, g

# We need to perform additional setup to the app, so we extract the 
# creation into a function.
def create_app():
    app = Flask(__name__)

    # To access the global context, you need to ensure that we're inside the 
    # Flask application context. It's a Flask thing you need to make 
    # setting up your database work.
    with app.app_context():
        get_db_session()

    print('Connected to Scylla!')

    return app 

def get_db_session():
    if 'db' not in g: 
        # Create a Cluster object with Scylla's address (localhost) and port
        cluster = Cluster(["127.0.0.1"], port=19042)

        # Connect to a specific keyspace on the cluster
        session = cluster.connect('reviews')

        # Save the db session in the Flask global context
        g.db = session
    
    return g.db

# Call our create_app function to create a Scylla connection
app = create_app()

# Route HTTP requests to '/' to this function
@app.route('/') 
def hello_world(): 
    # Return the name of the book
    # Flask automatically converts the value into an HTTP response
    return 'ScyllaDB in Action!' 