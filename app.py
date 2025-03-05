from flask import Flask, jsonify, request, redirect, url_for
import requests
import json
import os
from functools import wraps
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


# Função para validar o token JWT do Auth0
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", None)
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            response = requests.get(
                f'https://{app.config["AUTH0_DOMAIN"]}/userinfo',
                headers={"Authorization": f"Bearer {token}"},
            )
            user_info = response.json()
            if not user_info.get("sub"):
                raise Exception("Invalid token")
        except Exception as e:
            return jsonify({"message": str(e)}), 401

        return f(*args, **kwargs)

    return decorated


@app.route("/")
def home():
    return "API de Backend com Auth0 funcionando!"


@app.route("/private")
@requires_auth
def private():
    return jsonify({"message": "Você está autenticado!"})


@app.route("/login")
def login():
    return redirect(
        f"https://{app.config['AUTH0_DOMAIN']}/authorize?response_type=code&client_id={app.config['AUTH0_CLIENT_ID']}&redirect_uri={url_for('callback', _external=True)}"
    )


@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_url = f"https://{app.config['AUTH0_DOMAIN']}/oauth/token"
    headers = {"Content-Type": "application/json"}
    payload = {
        "client_id": app.config["AUTH0_CLIENT_ID"],
        "client_secret": app.config["AUTH0_CLIENT_SECRET"],
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": url_for("callback", _external=True),
    }

    response = requests.post(token_url, json=payload, headers=headers)
    response_data = response.json()

    access_token = response_data.get("access_token")

    return jsonify({"access_token": access_token})


if __name__ == "__main__":
    app.run(debug=True)
