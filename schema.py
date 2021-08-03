from datetime import datetime
from operator import add
import uuid

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema

from models import User, TopUp, Payment, Transfer, db

class UserRegisterSchema(SQLAlchemySchema):
    class Meta:
        model = User
        sqla_session = db.session
    user_id = fields.Str()
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    pin = fields.Str(required=True)
    balance = fields.Int()
    address = fields.Str(required=True)
    created_date = fields.Str()

    def register(self, data):
        user = User(**data)
        db.session.add(user)  # Adds new User record to database
        db.session.commit()
        return data


class TopUpSchema(SQLAlchemySchema):
    class Meta:
        model = TopUp


    def top_up(self, user, amount):
        if isinstance(amount, str):
            amount = int(amount)
        balance_after = user.balance + amount
        instance = TopUp(
            user_id=user.user_id,
            top_up_id=uuid.uuid4(),
            amount_top_up=amount,
            balance_before=user.balance,
            balance_after=balance_after,
            created_date=datetime.now()
        )
        user.balance = balance_after
        db.session.add(instance)
        db.session.commit()
        return {
            "top_up_id": instance.top_up_id,
            "amount_top_up": instance.amount_top_up,
            "balance_before": instance.balance_before,
            "balance_after": instance.balance_after,
            "created_date": instance.created_date
        }


class PaymentSchema(SQLAlchemySchema):

    class Meta:
        model = Payment

    def payment(self, user, amount, remarks):
        if isinstance(amount, str):
            amount = int(amount)
        balance_after = user.balance - amount
        if balance_after < 0:
            raise ValueError("Balance is not enough")
        instance = Payment(
            user_id=user.user_id,
            payment_id=uuid.uuid4(),
            amount=amount,
            balance_before=user.balance,
            balance_after=balance_after,
            remarks=remarks,
            created_date=datetime.now()
        )
        user.balance = balance_after
        db.session.add(instance)
        db.session.commit()
        return {
            "payment_id": instance.payment_id,
            "amount": instance.amount,
            "remarks": instance.remarks,
            "balance_before": instance.balance_before,
            "balance_after": instance.balance_after,
            "created_date": instance.created_date
        }


class TransferSchema(SQLAlchemySchema):

    class Meta:
        model = Transfer

    def transfer(self, user, target, amount, remarks):
        if isinstance(amount, str):
            amount = int(amount)
        target_user = User.query.filter_by(user_id=target).first()
        target_user.balance = target_user.balance + amount
        balance_after = user.balance - amount
        if balance_after < 0:
            raise ValueError("Balance is not enough")
        instance = Transfer(
            user_id=user.user_id,
            transfer_id=uuid.uuid4(),
            target_user=target,
            amount=amount,
            balance_before=user.balance,
            balance_after=balance_after,
            remarks=remarks,
            created_date=datetime.now()
        )
        user.balance = balance_after
        db.session.add(instance)
        db.session.commit()
        return {
            "transfer_id": instance.transfer_id,
            "amount": instance.amount,
            "remarks": instance.remarks,
            "balance_before": instance.balance_before,
            "balance_after": instance.balance_after,
            "created_date": instance.created_date
        }
