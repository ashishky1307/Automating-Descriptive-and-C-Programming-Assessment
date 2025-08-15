from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Flask app is running! 🎉"

@app.route('/test')
def test():
    return "Test route works!"

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5000)
