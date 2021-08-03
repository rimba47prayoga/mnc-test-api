import uuid
import json
from datetime import datetime, date
from flask import Flask, request, jsonify, make_response

from sqlalchemy import and_

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from models import db, User, Transactions
from schema import (
    TransferSchema,
    UserRegisterSchema,
    UserLoginSchema,
    TopUpSchema,
    PaymentSchema
)
from tasks import make_celery

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://rimba:qweqweqwe@localhost:3306/mnc_test'
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    result_backend='redis://localhost:6379'
)
db.init_app(app)
with app.app_context():
    db.create_all()

celery = make_celery(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


@celery.task
def record_transaction(user_id, data):
    instance = Transactions(
        id=uuid.uuid4(),
        user_id=user_id,
        json=data
    )
    db.session.add(instance)
    db.session.commit()


def serialize(o):
    if isinstance(o, (datetime, date)):
        return o.isoformat()


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    schema = UserRegisterSchema()
    try:
        schema.load(data)
    except ValidationError as err:
        return err.messages, 400
    exists = db.session.query(
        db.exists().where(User.phone_number == data.get("phone_number"))
    ).scalar()
    if exists:
        return {
            "message": "Phone Number already registered"
        }, 400

    data.update({
        "user_id": str(uuid.uuid4()),
        "created_date": str(datetime.now()),
        "balance": 0
    })
    
    user = schema.register(data)
    response = {
        "status": "SUCCESS",
        "result": schema.dump(user)
    }
    return make_response(jsonify(response))


@app.route("/login", methods=["POST"])
def login():
    try:
        UserLoginSchema().load(request.get_json())
    except ValidationError as err:
        return err.messages, 400
    phone_number = request.json.get("phone_number", None)
    pin = request.json.get("pin", None)

    exists = db.session.query(
        db.exists().where(and_(
            User.phone_number == phone_number,
            User.pin == pin
        ))
    ).scalar()
    if not exists:
        return {
            "message": "Phone number and pin doesn’t match."
        }, 400
    access_token = create_access_token(identity=phone_number)
    refresh_token = create_refresh_token(identity=phone_number)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@app.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    user = User.query.filter_by(
        phone_number=get_jwt_identity()
    ).first()
    data = request.get_json()
    user.first_name = data.get("first_name")
    user.last_name = data.get("last_name")
    user.address = data.get("address")
    user.updated_at = str(datetime.now())
    db.session.commit()
    return {
        "status": "SUCCESS",
        "result": {
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "address": user.address,
            "updated_at": user.updated_at
        }
    }


@app.route("/topup", methods=["POST"])
@jwt_required()
def topup():
    data = request.get_json()
    schema = TopUpSchema()
    try:
        data = schema.load(data)
    except ValidationError as err:
        return err.messages, 400
    current_user = User.query.filter_by(
        phone_number=get_jwt_identity()
    ).first()
    
    
    result = schema.top_up(current_user, data.get("amount"))

    # record transaction
    record_transaction.delay(
        current_user.user_id,
        json.dumps(
            {
                **result,
                "status": "SUCCESS",
                "transaction_type": "CREDIT",
                "remarks": "",
                "user_id": current_user.user_id
            },
            default=serialize
        )
    )
    response = {
        "status": "SUCCESS",
        "result": result
    }
    return jsonify(response), 201


@app.route("/pay", methods=["POST"])
@jwt_required()
def payment():
    data = request.get_json()
    schema = PaymentSchema()
    try:
        data = schema.load(data)
    except ValidationError as err:
        return err.messages, 400

    current_user = User.query.filter_by(
        phone_number=get_jwt_identity()
    ).first()
    
    try:
        result = schema.payment(
            current_user,
            data.get("amount"),
            data.get("remarks")
        )
    except ValueError as e:
        return {
            "message": e.args[0]
        }, 400
    else:
        response = {
            "status": "SUCCESS",
            "result": result
        }
        # record transaction
        record_transaction.delay(
            current_user.user_id,
            json.dumps(
                {
                    **result,
                    "status": "SUCCESS",
                    "transaction_type": "DEBIT",
                    "user_id": current_user.user_id
                },
                default=serialize
            )
        )
        return jsonify(response), 201


@app.route("/transfer", methods=["POST"])
@jwt_required()
def transfer():
    data = request.get_json()
    schema = TransferSchema()
    try:
        data = schema.load(data)
    except ValidationError as err:
        return err.messages, 400
    current_user = User.query.filter_by(
        phone_number=get_jwt_identity()
    ).first()
    
    try:
        result = schema.transfer(
            current_user,
            data.get("target_user"),
            data.get("amount"),
            data.get("remarks")
        )
    except ValueError as e:
        return {
            "message": e.args[0]
        }, 400
    else:
        response = {
            "status": "SUCCESS",
            "result": result
        }
        # record transaction
        record_transaction.delay(
            current_user.user_id,
            json.dumps(
                {
                    **result,
                    "status": "SUCCESS",
                    "transaction_type": "DEBIT",
                    "user_id": current_user.user_id
                },
                default=serialize
            )
        )
        return jsonify(response), 201


@app.route("/transactions", methods=["GET"])
@jwt_required()
def transactions():
    current_user = User.query.filter_by(
        phone_number=get_jwt_identity()
    ).first()
    items = Transactions.query.filter_by(user_id=current_user.user_id).all()
    result = []
    for item in items:
        try:
            result.append(json.loads(item.json))
        except Exception:
            result.append(item.json)
    response = {
        "status": "SUCCESS",
        "result": result
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
