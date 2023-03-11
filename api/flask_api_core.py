from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse
import pandas as pd
import logging as logging
import openai


openai.api_key = "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"


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


class summarize(Resource):
    # methods go here
    def get(self):
        arguments = request.args
        arguments = arguments.to_dict(flat=False)
        text = str(arguments["data"][0])
        data = summarize_text(text)
        response = make_response(data, 200)
        response.mimetype = "text/plain"
        return response  # return data and 200 OK code


class random_question(Resource):
    # methods go here
    def get(self):
        arguments = request.args
        arguments = arguments.to_dict(flat=False)
        text = str(arguments["data"][0])
        data = ask_me_anything(text)
        response = make_response(data, 200)
        response.mimetype = "text/plain"
        return response  # return data and 200 OK code

    pass


api.add_resource(summarize, "/summarize")
api.add_resource(random_question, "/question")

if __name__ == "__main__":
    app.run()  # run our Flask app