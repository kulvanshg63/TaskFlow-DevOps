from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>TaskFlow</h1>
    <p>DevOps Task Management System</p>
    <p>Application is running successfully.</p>
    """


if __name__ == "__main__":
    app.run(debug=True)

    