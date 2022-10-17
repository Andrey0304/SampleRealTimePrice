from flask import Flask

app = Flask(__name__)


@app.route("/")
def main():
    return 'OK Andrey'


if __name__ == "__main__":
    app.run(port=8000)
