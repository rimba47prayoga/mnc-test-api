from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.String(100), primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    phone_number = db.Column(db.String(20))
    pin = db.Column(db.String(10))
    address = db.Column(db.Text())
    balance = db.Column(db.Integer())
    created_date = db.Column(db.DateTime())
    updated_date = db.Column(db.DateTime())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"{self.user_id}"


class TopUp(db.Model):
    __tablename__ = "topup"
    user_id = db.Column(db.String(100))
    top_up_id = db.Column(db.String(100), primary_key=True)
    amount_top_up = db.Column(db.Integer())
    balance_before = db.Column(db.Integer())
    balance_after = db.Column(db.Integer())
    created_date = db.Column(db.DateTime())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"{self.top_up_id}"


class Payment(db.Model):
    __tablename__ = "payment"
    user_id = db.Column(db.String(100))
    payment_id = db.Column(db.String(100), primary_key=True)
    amount = db.Column(db.Integer())
    remarks = db.Column(db.String(100))
    balance_before = db.Column(db.Integer())
    balance_after = db.Column(db.Integer())
    created_date = db.Column(db.DateTime())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"{self.payment_id}"


class Transfer(db.Model):
    __tablename__ = "transfer"
    user_id = db.Column(db.String(100))
    transfer_id = db.Column(db.String(100), primary_key=True)
    target_user = db.Column(db.String(100))
    amount = db.Column(db.Integer())
    remarks = db.Column(db.String(100))
    balance_before = db.Column(db.Integer())
    balance_after = db.Column(db.Integer())
    created_date = db.Column(db.DateTime())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"{self.transfer_id}"


class Transactions(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    json = db.Column(db.Text())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"{self.id}"
