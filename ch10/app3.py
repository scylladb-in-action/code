# Importing the execution profile allows you to override the 
# cluster's options
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT

# The dict_factory instructs the driver to return rows as dictionaries
from cassandra.query import dict_factory

from flask import Flask, g

# We need to perform additional setup to the app, so we extract the 
# creation into a function.
def create_app():
    app = Flask(__name__)

    with app.app_context():
        get_db_session()

    print('Connected to Scylla!')

    return app 

def get_db_session():
    if 'db' not in g: 
        # The execution profile allows you to override the driver's 
        # behavior
        profile = ExecutionProfile(
            # The dict_factory option tells the driver to return rows as a 
            # dictionary
            row_factory=dict_factory
        )

        # Passing the profile to the cluster applies the options 
        # specified in your profile
        cluster = Cluster(
            ["127.0.0.1"], 
            port=9042, 
            # EXEC_PROFILE_DEFAULT is the default profile used
            execution_profiles={EXEC_PROFILE_DEFAULT: profile}
        )

        # Connect to a specific keyspace on the cluster
        session = cluster.connect('reviews')

        # Save the db session in the Flask global context
        g.db = session
    
    return g.db

# Call your create_app function to create a Scylla connection
app = create_app()

@app.route('/authors')
def authors():
    # Retrieve the database 
    db = get_db_session()

    # Execute the query, returning a result set 
    result_set = db.execute('SELECT * FROM authors')

    authors = []

    # Iterate through the result set and add the authors into a list
    for row in result_set:
        authors.append(row)
        
    # Return the retrieved authors, which Flask automatically converts
    # to JSON 
    return authors

@app.route('/') 
def hello_world(): 
    return 'ScyllaDB in Action!' 