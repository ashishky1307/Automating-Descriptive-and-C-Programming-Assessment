from flask import Flask
from models import db
from routes import main
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Register Blueprints
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=False)
