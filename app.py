# Import Flask dependency
from flask import Flask

# Create new Flask app instance
app = Flask(__name__)

# Define starting point, or root, for first route
@app.route('/')
def hello_world():
    return 'Hello world'