from flask import render_template, url_for, flash, redirect, request, abort
from mwas import app, db, bcrypt, login_manager, admin, mail
import os
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from PIL import Image
from mwas.models import (User, Administrator, grow, Farmer, Farmer_crops, Customer,
                         Crops_of_interest, Compliant, Post, Order, Marketing_stat_rp,
                         Marketing_stat_wp, Advert, Market_available
                         )
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from mwas.forms import (RegistrationForm, LoginForm, AdminForm, QueryForm,
                        RequestResetForm, ResetPasswordForm, ComplaintForm, CropsForm,
                        EmailForm, AdvertForm, SendMessageForm, PostForm, UpdateAccountForm,
                        QueryMarketForm, MarketCustomerForm, Sys_message
                        )
from flask_mail import Message
# from werkzeug import secure_filename
from werkzeug.utils import secure_filename
import nexmo


class AdvertsView(BaseView):
    @expose('/')
    def index(self):
        """ Shows adverts sent by farmers """
        data = Advert.query.order_by(Advert.date.desc()).all()
        if data:
            flash(
                'This a web page that shows details about Adverts sent by users(Farmers) of the System',
                'info'
            )
            return render_template('admin_advert.html', title="Adverts", data=data)
        return self.render('admin_advert.html', admin=admin)


class AdvertCustomerView(BaseView):
    @expose('/')
    def index(self):
        """ Shows requests sent by customers"""
        data = Market_available.query.order_by(Market_available.date.desc()).all()
        if data:
            flash(
                'Shows details about Adverts sent by users(Wholesalers, Retailers etc.) of the System',
                'info'
            )
            return render_template('admin_customer.html', title="Adverts", data=data)
        return self.render('admin_customer.html', admin=admin)


class SendMarketAlertsView(BaseView):
    @expose('/', methods=["GET", "POST"])
    def index(self):
        """ used to send sms alerts to farmers """
        Api_key = "21ef5c10"
        Api_secret = "1UiKqvMacdfh5aPp"
        form = SendMessageForm()
        if form.validate_on_submit():
            sender = form.sender.data
            to = form.number.data
            text = form.text.data
            f = Sys_message(sender, to)
            f.Send_message(text)
            return render_template('market.html', title="Adverts", form=form)
        return self.render('market.html', form=form, admin=admin)


class SendEmailView(BaseView):
    @expose('/', methods=["GET", "POST"])
    def index(self):
        """ Function used to send emails"""
        form = EmailForm()
        if form.validate_on_submit():
            msg = Message(form.subject.data, sender=form.sender.data,
                          recipients=[form.receiver.data])
            msg.body = form.message.data
            mail.send(msg)
            flash("E-mail sent", "success")
        return self.render('admin_email.html', title='Email', form=form, admin=admin)


def access():
    user = Administrator.query.filter_by(username=current_user.username).first()
    if user:
        return True
    else:
        False


class MyModelView(ModelView):
    def is_accessible(self):
        return access()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Administrator, db.session))
admin.add_view(MyModelView(Farmer, db.session))
admin.add_view(MyModelView(Farmer_crops, db.session))
admin.add_view(MyModelView(Customer, db.session))
admin.add_view(MyModelView(Crops_of_interest, db.session))
admin.add_view(MyModelView(Compliant, db.session))
admin.add_view(MyModelView(Post, db.session))
admin.add_view(MyModelView(Order, db.session))
admin.add_view(MyModelView(Marketing_stat_rp, db.session))
admin.add_view(MyModelView(Marketing_stat_wp, db.session))
admin.add_view(MyModelView(Market_available, db.session))
admin.add_view(MyModelView(Advert, db.session))
admin.add_view(AdvertCustomerView('Adverts(Customers)', url='/adverts_customers'))
admin.add_view(AdvertsView('Adverts(Farmers)', url='/adverts'))
admin.add_view(SendMarketAlertsView(' Send Market Adverts (SMS)', url='/markets'))
admin.add_view(SendEmailView('Send Email to User', url='/email'))


# @app.route("/")
@app.route("/home_blog")
def home_blog():
    """ routes you to the blog site """
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home_blog.html', posts=posts)


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    """ Function used to post a blog"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created", "success")
        return redirect(url_for("home_blog"))
    return render_template("create_post.html", title="New Post", form=form, legend="New Post")


@app.route("/user/<string:username>")
def user_posts(username):
    """ Get posts based on a user"""
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@app.route("/post/<int:post_id>")
def post(post_id):
    """ Get all posts """
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


def save_picture2(form_picture):
    """ Function used to save a picture """
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f_name + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account_blog", methods=['GET', 'POST'])
@login_required
def account_blog():
    """ Update account details """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture2(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your Account has been updated!", "success")
        return redirect(url_for("account_blog"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """ Function used to authenticate users of the system """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            farmer = Farmer.query.filter_by(id=current_user.id).first()
            picture_file = save_picture2(form.picture.data)
            current_user.image_file = picture_file
        farmer.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your Account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("faaccount.html", title="Account", image_file=image_file, form=form)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    """ update a post """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been Updated!", "success")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")


# @app.route("/about")
# def about():
# return render_template('about.html', title="About")
@app.route("/home")
def home():
    return render_template('home.html', title="Home")


@app.route("/farm", methods=['GET', 'POST'])
def farm():
    form = EmailForm()
    if form.validate_on_submit():
        msg = Message(form.subject.data, sender=form.sender.data,
                      recipients=[form.receiver.data])
        msg.body = form.message.data
        ##        with app.open_resource(os.path.abspath(form.attachment.data)) as fp:
        ##            f_name = form.attachment.data.split('.')
        ##            msg.attach(form.attachment.data,f_name[0]+'/'+f_name[1],fp.read())
        mail.send(msg)
        flash("E-mail sent", "success")
    return render_template('farmer.html', title='Farmer', form=form)


@app.route("/MWASdataxxcAdmin", methods=['GET', 'POST'])
# @login_required
def MWASdataxxcAdmin():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = AdminForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Administrator(first_name=form.first_name.data, last_name=form.last_name.data,
                              username=form.username.data,
                              email=form.email.data, password=hashed_password)
        user = User(username=form.username.data, email=form.email.data, sign_in_as="Admin", password=hashed_password)
        db.session.add(user)
        db.session.add(admin)
        db.session.commit()
        flash("Your Account has been Created! You are now able to log in", "success")
        return redirect(url_for('login'))
    return render_template("register_admin.html", title="RegisterAdmin", form=form)


@app.route("/register_farmer", methods=['GET', 'POST'])
def register_farmer():
    """ Register a user i.e farmer, wholesaler or retailer"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.sigin.data == "Farmer":
            user = User(
                username=form.username.data,
                email=form.email.data,
                sign_in_as=form.sigin.data,
                password=hashed_password
            )
            farmer = Farmer(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                phone_number=form.pnumber.data,
                physical_address=form.physical_add.data
            )
            db.session.add(farmer)
            db.session.add(user)
            db.session.commit()
            flash("Your Account has been Created! You are now able to log in", "success")
        elif form.sigin.data == "Wholesaler":
            user = User(
                username=form.username.data,
                email=form.email.data,
                sign_in_as=form.sigin.data,
                password=hashed_password
            )
            customer = Customer(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                phone_number=form.pnumber.data,
                physical_address=form.physical_add.data
            )
            db.session.add(customer)
            db.session.add(user)
            db.session.commit()
            flash("Your Account has been Created! You are now able to log in", "success")
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Used to authenticate users of the system"""
    if current_user.is_authenticated:
        return redirect(url_for('farm'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.sigin.data == "Farmer":
            user = User.query.filter_by(username=form.username.data).first()
            farmer = Farmer.query.filter_by(username=form.username.data).first()
            if farmer:
                check_password = bcrypt.check_password_hash(user.password, form.password.data)
                if check_password:
                    flash("You have been Logged in!", "success")
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('farm'))
                else:
                    flash("Login Unsuccessful. Please check Username and Password", "danger")
                    return redirect(url_for('login'))

            else:
                flash("You don't belong to this category", "danger")
                return redirect(url_for('login'))
        elif form.sigin.data == "Wholesaler":
            user = User.query.filter_by(username=form.username.data).first()
            customer = Customer.query.filter_by(username=form.username.data).first()
            if customer:
                check_password = bcrypt.check_password_hash(user.password, form.password.data)
                if check_password:
                    flash("You have been Logged in!", "success")
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('customer'))
                else:
                    flash("Login Unsuccessful. Please check Username and Password", "danger")
                    return redirect(url_for('login'))
            else:
                flash("You don't belong to this category", "danger")
                return redirect(url_for('login'))
        elif form.sigin.data == "Admin":
            user = User.query.filter_by(username=form.username.data).first()
            admin = Administrator.query.filter_by(username=form.username.data).first()
            if admin:
                check_password = bcrypt.check_password_hash(admin.password, form.password.data)
                if check_password:
                    flash("You have been Logged in!", "success")
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('admin.index'))
                else:
                    flash("Login Unsuccessful. Please check Username and Password", "danger")
                    return redirect(url_for('login'))
            else:
                flash("You don't belong to this category", "danger")
                return redirect(url_for('login'))
    return render_template("login.html", title="login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/charts", methods=['GET', 'POST'])
@login_required
def charts():
    """ Display charts """
    form = QueryForm()
    if form.validate_on_submit():
        chart_data1 = Marketing_stat_rp.query.filter_by(comodity=form.query.data).first()
        chart_data2 = Marketing_stat_wp.query.filter_by(comodity=form.query.data).first()
        list1 = Marketing_stat_rp.query.all()
        list2 = Marketing_stat_wp.query.all()
        all_items = [list1, list2]
        query_list = [chart_data1, chart_data2]
        return render_template(
            'charts.html',
            title="MWAS charts",
            query_list=query_list,
            all_items=all_items
        )
    return render_template('query.html', form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='jbyenkyaaaron@gmail.com',
                  recipients=[user.email])
    msg.body = "To reset your password visit the following link " + url_for(
        'reset_token',
        token=token,
        _external=True) + "\n if you did not request for this email then ignore."
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """ Get a token to reset password """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!\n your able to login!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route("/complaint", methods=['GET', 'POST'])
# @login_required
def complaint():
    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Compliant(
            user_category=form.user_category.data,
            username=form.username.data,
            compliant=form.comment.data,
            status="Pending",
            user_id=current_user.id
        )
        db.session.add(complaint)
        db.session.commit()
        flash('Your complaint has been received', 'success')
        return redirect(url_for('complaint'))
    return render_template('complaint.html', title='Complaint', form=form)


def save_picture(form_picture):
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f_name + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/crops", methods=['GET', 'POST'])
def crops():
    form = CropsForm()
    if form.validate_on_submit():
        picture = save_picture(form.picture.data)
        farmer = Farmer.query.filter_by(username=current_user.username).first()
        crop = Farmer_crops(
            crop_type=form.crop_type.data,
            quantity=form.quantity.data,
            image_file=form.picture.data.filename,
            user_id=current_user.id
        )
        db.session.add(crop)
        crop.grows.append(farmer)
        db.session.commit()
        flash('Your products have been Stored', 'success')
        return redirect(url_for('crops'))
    return render_template('store.html', title='Store', form=form)


@app.route("/status")
def status():
    data = Compliant.query.filter_by(username=current_user.username).all()
    if data:
        return render_template('status.html', title="Status of Complaints", data=data)
    else:
        flash('No complaints', 'info')
        return redirect(url_for('farm'))



@app.route("/advert", methods=['GET', 'POST'])
def advert():
    form = AdvertForm()
    if form.validate_on_submit():
        picture = save_picture(form.picture.data)
        advert = Advert(
            username=form.username.data,
            contact=form.contact.data,
            email=current_user.email,
            Description=form.commodity.data,
            image_file=form.picture.data.filename,
            user_id=current_user.id
        )
        db.session.add(advert)
        db.session.commit()
        flash('Advert Recieved You will be notified incase of any Available Market', 'info')
        return redirect(url_for('advert'))
    return render_template('advert.html', title="Advert", form=form)


@app.route("/search_market", methods=['GET', 'POST'])
def search_market():
    """Search for available markets """
    form = QueryMarketForm()
    if form.validate_on_submit():
        crop = Market_available.query.filter_by(crop=form.query.data).all()
        return render_template("available.html", title="Makert Information", crop=crop)
    return render_template("mk.html", title="Makert Information", form=form)


###############################################################################################################
# customers functionality.

@app.route("/customer", methods=["GET", "POST"])
def customer():
    form = EmailForm()
    if form.validate_on_submit():
        msg = Message(
            form.subject.data,
            sender=form.sender.data,
            recipients=[form.receiver.data]
        )
        msg.body = form.message.data
        mail.send(msg)
        flash("E-mail sent", "success")
    return render_template("customer_dash.html", title="Customer", form=form)


@app.route("/view_farmer", methods=['GET', 'POST'])
def view_farmer():
    form = QueryMarketForm()
    if form.validate_on_submit():
        query = form.query.data
        data = Farmer.query.join(grow).join(Farmer_crops).filter_by(crop_type=form.query.data).all()
        if data:
            return render_template("view_farmers.html", title="Farmers", data=data, query=query)
        else:
            flash("There are no Farmers for that Crop in the System at the moment", "warning")
            return redirect(url_for('view_farmer'))
    return render_template("mk.html", title="Market Information", form=form)


@app.route("/advert_customer", methods=['GET', 'POST'])
def advert_customer():
    form = MarketCustomerForm()
    if form.validate_on_submit():
        picture = save_picture(form.picture.data)
        advert = Market_available(
            names=form.names.data,
            email=form.email.data,
            contact=form.contact.data,
            crop=form.crop.data,
            description=form.description.data,
            image_file=form.picture.data.filename,
            user_id=current_user.id
        )
        db.session.add(advert)
        db.session.commit()
        flash('Advert Received You will be notified incase of any Available Market', 'info')
        return redirect(url_for('advert_customer'))
    return render_template('admin_advert_customer.html', title="Advert", form=form)
