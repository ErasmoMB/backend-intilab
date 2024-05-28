./

# tengo un error en la pc de mi casa consultando los autores y documentos, tengo la imagen del error que me da y aqui esta la ruta

# aqui esta la url: https://api.elsevier.com/content/search/author?query=AF-ID(60110778)&apiKey=b21b68bd3eb1b573af7f883b0c9b70d7

# usar esto para activar el entorno virtual .\venv\Scripts\activate

# mongod para que el mongoose corra   1 terminal
# python src/app.py  para ejecutar    2 terminal
# mongosh para acceder al chat interactivo de mongodb 3 terminal
# *show databases
# *use database
# *show collections
# *db.users.find()


# Codigo de app como ejemplo para hacer crud a mongo en un archivo llamado app dentro de src app.py

from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost/investigadoresmongodb"
mongo = PyMongo(app)


@app.route("/users", methods=["POST"])
def create_user():
    # Recibiendo datos
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]

    if username and email and password:
        hashed_password = generate_password_hash(password)
        result = mongo.db.users.insert_one(
            {"username": username, "email": email, "password": hashed_password}
        )
        id = result.inserted_id
        response = {
            "id": str(id),
            "username": username,
            "password": hashed_password,
            "email": email,
        }
        return response
    else:
        return {"message": "received"}


@app.route("/users", methods=["GET"])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")


@app.route("/users/<id>", methods=["GET"])
def get_user(id):
    user = mongo.db.users.find_one({"_id": ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    mongo.db.users.delete_one({"_id": ObjectId(id)})
    response = jsonify({"message": "User " + id + " was deleted successfully"})
    return response

@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    if username and email and password:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"username": username, "email": email, "password": hashed_password}},
        )
        response = jsonify({"message": "User " + id + " was updated successfully"})
        return response


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({"message": "Resource Not Found: " + request.url, "status": 404})
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)


# Codigo de models

""" # models/author_details.py
import boto3
from bson import json_util
from bson.objectid import ObjectId

def create_author_details(db, author_id, image, academic_degree):
    # Cargar la imagen a S3
    s3 = boto3.client('s3')
    with open(image, "rb") as data:
        s3.upload_fileobj(data, 'se-autores', image)

    # Guardar el detalle del autor en la base de datos
    result = db.author_details.insert_one(
        {"author_id": author_id, "image": 'https://se-autores.s3.amazonaws.com/' + image, "academic_degree": academic_degree}
    )
    id = result.inserted_id
    response = {
        "id": str(id),
        "author_id": author_id,
        "image": 'https://s3-autores.s3.amazonaws.com/' + image,
        "academic_degree": academic_degree,
    }
    return response

def get_author_details(db):
    author_details = db.author_details.find()
    response = json_util.dumps(author_details)
    return response

def get_author_detail(db, id):
    author_detail = db.author_details.find_one({"_id": ObjectId(id)})
    response = json_util.dumps(author_detail)
    return response

def delete_author_detail(db, id):
    db.author_details.delete_one({"_id": ObjectId(id)})
    response = {"message": "Author Detail " + id + " was deleted successfully"}
    return response

def update_author_detail(db, id, author_id, image, academic_degree):
    db.author_details.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"author_id": author_id, "image": image, "academic_degree": academic_degree}},
    )
    response = {"message": "Author Detail " + id + " was updated successfully"}
    return response """


# Database 

""" # database/db.py
from flask_pymongo import PyMongo

def get_db(app):
    app.config["MONGO_URI"] = "mongodb://localhost/investigadoresmongodb"
    mongo = PyMongo(app)
    return mongo """