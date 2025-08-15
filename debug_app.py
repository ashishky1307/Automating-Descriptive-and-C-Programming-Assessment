from flask import Flask
import sys
import traceback

print("Starting imports...")

try:
    from models import db
    print("✓ Models imported successfully")
except Exception as e:
    print(f"✗ Error importing models: {e}")
    sys.exit(1)

try:
    from routes import main
    print("✓ Routes imported successfully")
except Exception as e:
    print(f"✗ Error importing routes: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    from config import Config
    print("✓ Config imported successfully")
except Exception as e:
    print(f"✗ Error importing config: {e}")
    sys.exit(1)

app = Flask(__name__)
app.config.from_object(Config)

print("Initializing database...")
# Initialize database
db.init_app(app)

print("Registering blueprints...")
# Register Blueprints
app.register_blueprint(main)

print("Flask app setup complete!")

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
