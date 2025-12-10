from flask import Flask
from lse import lse
from rootfinding import rootf

app = Flask(__name__)

app.register_blueprint(lse)
app.register_blueprint(rootf)

from flask_cors import CORS
CORS(app, resources={r"/*": {"origins": "*"}})  


# if app.name == "__main__" :
app.run(debug= True, port= 8080)

