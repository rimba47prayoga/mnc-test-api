import uuid
import json
from datetime import datetime, date
from flask import Flask, request, jsonify, make_response

from sqlalchemy import and_

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from models import db, User, Transactions
from schema import TransferSchema, UserRegisterSchema, TopUpSchema, PaymentSchema
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
def record_transaction(data):
    instance = Transactions(id=uuid.uuid4(), json=data)
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
        return err, 400
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
    return jsonify(access_token=access_token)


@app.route("/topup", methods=["POST"])
@jwt_required()
def update_profile():
    current_user = User.query.filter_by(
        phone_number=get_jwt_identity()
    ).first()
    data = request.get_json()


@app.route("/topup", methods=["POST"])
@jwt_required()
def topup():
    current_user = User.query.filter_by(
        phone_number=get_jwt_identity()
    ).first()
    data = request.get_json()
    schema = TopUpSchema()
    result = schema.top_up(current_user, data.get("amount"))

    # record transaction
    record_transaction.delay(
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
    current_user = User.query.filter_by(
        phone_number=get_jwt_identity()
    ).first()
    data = request.get_json()
    schema = PaymentSchema()
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
    current_user = User.query.filter_by(
        phone_number=get_jwt_identity()
    ).first()
    data = request.get_json()
    schema = TransferSchema()
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


if __name__ == "__main__":
    app.run(debug=True)
