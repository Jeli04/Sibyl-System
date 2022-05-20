import json
from flask import Flask, render_template, request, jsonify, url_for

from chat import chatbot_response

app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("index.html")

@app.get("/sad")
def sad_get():
    return render_template("sad.html")

@app.get("/about")
def about_sibyl_get():
    return render_template("sibylinfo.html")

@app.get("/forum")
def forum_get():
    return render_template("forum.html")



@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    print("predict text: ", text)
    response = chatbot_response(text)
    message = {"answer": response}
    return jsonify(message)



if __name__ == "__main__":
    app.run(debug=True)
