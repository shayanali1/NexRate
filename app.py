from flask import Flask

app = Flask(__name__)
app.secret_key = "nexrate_secret_key"

@app.route("/")
def index():
    return "NexRate is running!"

if __name__ == "__main__":
    app.run(debug=True)