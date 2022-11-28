from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin,AdminIndexView
##from flask_admin.contrib.sqla import ModelView
#from mwas.models import User,Farmer,Farmer_crops,Customer,Crops_of_interest,Compliant,Post,Order,Marketing_stat_rp,Marketing_stat_wp
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail 
#from sqlalchemy.sql import func
app = Flask(__name__)
app.config["SECRET_KEY"] = "XNDKUJDJ84y2h298yy39001hcbc"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///msaw.sqlite3'
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_ASCII_ATTACHMENTS'] = True
app.config['MAIL_USERNAME'] = 'jbyenkyaaaron@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'jbyenkyaaaron@gmail.com'
app.config['MAIL_PASSWORD'] = "jb@aaron123"
mail = Mail(app)
admin = Admin(app, name="Market Survey Assistant Web Service \n DashBoard")
from mwas import routes


