from mwas import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import URLSafeTimedSerializer as Serializer
#https://oddslot.com/odds/
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Administrator(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="123.jpg")
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return self.username
    
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="123.jpg")
    sign_in_as = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref="author", lazy=True)
    complian = db.relationship('Compliant', backref="auth1", lazy=True)
    order = db.relationship("Order", backref="orders", lazy=True)
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    @staticmethod #not to expect the self argument.
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    def __repr__(self):
        return "User("+self.username+","+self.email+")"

grow = db.Table('grows',
        db.Column('farmer_id', db.Integer, db.ForeignKey('farmer.id')),
        db.Column('crop_id', db.Integer, db.ForeignKey('crops.id'))
        )

class Farmer(db.Model):
    __tablename__ = "farmer"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, index=True, nullable=False)
    physical_address = db.Column(db.String(100), index=True,nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="123.jpg")
    grows = db.relationship('Farmer_crops', secondary=grow, backref=db.backref("grows", lazy='dynamic'))
    advert = db.relationship('Advert', backref="advertise", lazy=True)
    def __repr__(self):
        return "Farmer("+self.username+","+self.email+","+self.physical_address+")"
    
class Farmer_crops(db.Model):
    __tablename__ = "crops"
    id = db.Column(db.Integer, primary_key=True)
    crop_type = db.Column(db.String(20), index=True,nullable=False)
    quantity = db.Column(db.String(15), index=True,nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default="123.jpg")
    user_id = db.Column(db.Integer, db.ForeignKey('farmer.id'), nullable=False)

interest = db.Table('interested',
        db.Column('customer_id', db.Integer, db.ForeignKey('customer.id')),
        db.Column('crop_of_id', db.Integer, db.ForeignKey('interests.id'))
        )

class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, index=True, nullable=False)
    physical_address = db.Column(db.String(100), index=True,nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="123.jpg")
    interested = db.relationship('Crops_of_interest', secondary=interest, backref=db.backref("interested_in", lazy='dynamic'))
    advert = db.relationship('Market_available', backref="advertise", lazy=True)
    def __repr__(self):
        return "Customer("+self.username+","+self.email+","+self.physical_address+","+self.agric_produce+")"

class Crops_of_interest(db.Model):
    __tablename__ = "interests"
    id = db.Column(db.Integer, primary_key=True)
    items_of_interest = db.Column(db.String(20), index=True,nullable=False)
    quantity = db.Column(db.String(15), index=True,nullable=True)

class Compliant(db.Model):
    __tablename__ = "compliant"
    id = db.Column(db.Integer, primary_key=True)
    user_category = db.Column(db.String(64), index=True, nullable=False)
    username = db.Column(db.String(64), index=True, nullable=False)
    compliant = db.Column(db.String(64), index=True, nullable=False)
    date_posted = db.Column(db.DateTime,index=True, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(10), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return "Farmer("+self.username+","+self.compliant+","+","+self.status+")"

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Post("+self.title+","+self.date_posted.strftime("%m/%d/%y")+")"

class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    trans_detail = db.Column(db.String(130),index=True, nullable=False)
    order_date = db.Column(db.DateTime,index=True, nullable=False, default=datetime.utcnow)
    order_state = db.Column(db.String(10), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return "Order("+self.trans_detail+","+self.order_date.strftime("%m/%d/%y")+","+self.order_state+")"
    
class Advert(db.Model):
    __tablename__ = "advert"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), index=True, nullable=False)
    Description = db.Column(db.String(5000), nullable=False)
    date = db.Column(db.DateTime,index=True, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=False, default="123.jpg")
    user_id = db.Column(db.Integer, db.ForeignKey('farmer.id'), nullable=False)

    def __repr__(self):
        return self.Description
    
class Marketing_stat_rp(db.Model):
    __tablename__ = "retailprice"
    id = db.Column(db.Integer, primary_key=True)
    comodity = db.Column(db.String(20),unique=True,nullable=False)
    units = db.Column(db.String(5),nullable=False)
    values = db.Column(db.String(5), nullable=False)
    average = db.Column(db.Integer(),nullable=True)
    central = db.Column(db.Integer(),nullable=True)
    eastern = db.Column(db.Integer(),nullable=True)
    northern = db.Column(db.Integer(),nullable=True)
    western = db.Column(db.Integer(),nullable=True)

    def __repr__(self):
        return self.units
    
class Marketing_stat_wp(db.Model):
    __tablename__ = "wholesaleprice"
    id = db.Column(db.Integer, primary_key=True)
    comodity = db.Column(db.String(20),unique=True,nullable=False)
    units = db.Column(db.String(5),nullable=False)
    values = db.Column(db.String(5), nullable=False)
    average = db.Column(db.Integer(),nullable=True)
    central = db.Column(db.Integer(),nullable=True)
    eastern = db.Column(db.Integer(),nullable=True)
    northern = db.Column(db.Integer(),nullable=True)
    western = db.Column(db.Integer(),nullable=True)

    def __repr__(self):
        return self.units
    
class Market_available(db.Model):
    __tablename__ = "availablemarkets"
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(120), index=True, nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    crop = db.Column(db.String(15), nullable=False)
    description = db.Column(db.String(2000),nullable=False)
    date = db.Column(db.DateTime,index=True, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=False, default="123.jpg")
    user_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    def __repr__(self):
        return self.description
    
    
    
if __name__ == '__main__':
    app.run(debug=True)












    
