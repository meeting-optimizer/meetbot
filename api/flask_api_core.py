from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api, reqparse
import pandas as pd
import logging as logging
import openai
from flask_cors import CORS

# protect your keys!!!!!
openai.api_key = "sk-xxx"


def summarize_text(text: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": f"Summarize: {text}"},
        ],
    )
    return "".join(choice.message.content for choice in response.choices)


def ask_me_anything(text: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": f"{text}"},
        ],
    )
    return "".join(choice.message.content for choice in response.choices)


app = Flask(__name__)
api = Api(app)
CORS(app)


class summarize(Resource):
    # methods go here
    def get(self):
        arguments = request.args
        arguments = arguments.to_dict(flat=False)
        text = str(arguments["data"][0])
        data = {"data": summarize_text(text)}
        return jsonify(data)


class random_question(Resource):
    # methods go here
    def get(self):
        arguments = request.args
        arguments = arguments.to_dict(flat=False)
        text = str(arguments["data"][0])
        data = {"data": ask_me_anything(text)}
        return jsonify(data)


api.add_resource(summarize, "/summarize")
api.add_resource(random_question, "/question")

if __name__ == "__main__":
    app.run()  # run our Flask app
    app.use(cors())
