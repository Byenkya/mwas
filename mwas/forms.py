from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,SelectField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from mwas.models import User,Marketing_stat_wp
import nexmo
from flask import flash
from mwas import app
#http://www.ukbettips.co.uk/todays-bet-tips.html
class RegistrationForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2,max=15)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2,max=15)])
    username = StringField("Username", validators=[DataRequired(), Length(min=2,max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pnumber = StringField("Phone number",validators=[DataRequired(),Length(min=10,max=15)])
    physical_add = StringField("Physical Address",validators=[DataRequired(),Length(min=4,max=30)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",
                        validators=[DataRequired(),EqualTo('password')])
    sigin = SelectField("Register as", validators=[DataRequired()], choices=[('Wholesaler','Wholesaler'),('Farmer','Farmer')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user  = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("User name taken choose another one!")
    def validate_email(self, email):
        user  = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email exits choose use another one!")
class AdminForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2,max=15)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2,max=15)])
    username = StringField("Username", validators=[DataRequired(), Length(min=2,max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user  = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("User name taken choose another one!")
    def validate_email(self, email):
        user  = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email exits choose use another one!") 
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2,max=15)])
    password = PasswordField("Password", validators=[DataRequired()])
    sigin = SelectField("Sign in as", validators=[DataRequired()], choices=[('Admin','Admin'),('Farmer','Farmer'),('Wholesaler','Wholesaler')])
    remember = BooleanField("Remember me")
    submit = SubmitField('Login')

class QueryForm(FlaskForm):
    with app.app_context():
        data = []
        # data = Marketing_stat_wp.query.all()
        choices = []
        count = 0
        if data:
            for item in data:
                como = (item.comodity, item.comodity)
                choices.append(como)
    query = SelectField("Search", validators=[DataRequired()], choices=choices)
    submit = SubmitField('Search')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user  = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. You must register first")
class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",
                        validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')

class ComplaintForm(FlaskForm):
    user_category = SelectField("Signed as",validators=[DataRequired(), Length(min=2,max=15)],choices=[('Wholesaler','Wholesaler'),('Farmer','Farmer')])
    username = StringField("Username", validators=[DataRequired(), Length(min=2,max=15)])
    comment = TextAreaField("Complaint", validators=[DataRequired()])
    submit = SubmitField('Submit Complaint')
    
class CropsForm(FlaskForm):
    crop_type = StringField('Enter crop for sale', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    picture = FileField("Crop Picture", validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Save Data')
class EmailForm(FlaskForm):
    sender = StringField('Your Email', validators=[DataRequired(), Email()])
    receiver = StringField('Recipient Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject',validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    #attachment = FileField("Attachment", validators=[FileAllowed(['jpg','png','txt','pdf','docx'])])
    submit = SubmitField('Send')
    
class AdvertForm(FlaskForm):
    username = StringField("Enter Your Names:", validators=[DataRequired()])
    contact = StringField("Phone number", validators=[DataRequired(), Length(min=10,max=15)])
    commodity = TextAreaField("Product Description:",validators=[DataRequired()])
    picture = FileField("Enter Picture of Product you want:", validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Post Advert')

class SendMessageForm(FlaskForm):
    sender = SelectField("Sender",validators=[DataRequired()],
                        choices=[('MWAS','MARKETING ASSISTANT WEB SERVICE')])
    number = StringField("Phone Number", validators=[DataRequired(), Length(min=2,max=15)])                         
    text = SelectField("Message Type", validators=[DataRequired()],
                       choices=[('Dear Customer there is Market For your Products. Login into your account to get more details.','Market Alert')])
    submit = SubmitField('Send Message')

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")
    
class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2,max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:   
            user  = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("User name taken choose another one!")
    def validate_email(self, email):
        if email.data != current_user.email:
            user  = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email exits choose use another one!")

class MarketCustomerForm(FlaskForm):
    names = StringField("Enter Your Names:", validators=[DataRequired(), Length(min=5,max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact = contact = StringField("Phone number", validators=[DataRequired(), Length(min=10,max=15)])
    crop = StringField("Enter Crop you Want:", validators=[DataRequired()])
    description = TextAreaField("Enter Product Description:",validators=[DataRequired()])
    picture = FileField("Enter Picture of Products:", validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Post Advert')

class QueryMarketForm(FlaskForm):
    query = StringField("Search", validators=[DataRequired()])
    submit = SubmitField('Search')

class Sys_message:
    def __init__(self,names,Client_number,Api_key = "21ef5c10",Api_secret = "1UiKqvMacdfh5aPp"):
        self.Names = names
        self.Client = Client_number
        self.api_key = Api_key
        self.secret = Api_secret
        #f = Sys_message("Byenkya","+256753919546")
        #f.Send_message("Yo watsap,how are you doing?")
    def Send_message(self,text):
        client = nexmo.Client(key=self.api_key,secret=self.secret)
        response = client.send_message({"from":self.Names,
                                        "to":self.Client,"text":text})
        response = response["messages"][0]
        if response["status"] == "0":
            print(response)
            flash("Message Sent","info")
##            print("Sent Message",response["message-id"])
##            print("Remaining Balance is",response["remaining-balance"])
        else:
            flash("Message not sent","danger")
            #print("Error",response["error-string"])






































            
