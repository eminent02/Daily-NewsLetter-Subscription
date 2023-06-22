from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import boto3, s3fs
import os
from dotenv import load_dotenv
load_dotenv()

client = boto3.client("ses", region_name='us-east-1', aws_access_key_id=os.getenv("ACCESS_KEY"),aws_secret_access_key= os.getenv("SECRET_KEY"))
status = "Unknown. Please click below check the status"
application = Flask(__name__)

application.secret_key = os.environ['APP_SECRET_KEY']

application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.app_context().push()

DATABASE = {
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
      }
database_url = 'mysql+pymysql://%(USER)s:%(PASSWORD)s@%(HOST)s:%(PORT)s/%(NAME)s' % DATABASE

application.config ['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(application)


# Defining TABLE structure
class User(db.Model):  
    name = db.Column(db.String(100))
    email = db.Column(db.String(50), primary_key = True)  
    news_category = db.Column(db.String(200))
    def __init__(self, name, email, news_category):
        self.name = name
        self.email = email
        self.news_category = news_category

db.create_all()

@application.route("/")
def index():
    return render_template("index.html")

@application.route("/validate-user", methods=["POST"])
def validate_user():
    if request.method == "POST":
        user_input = request.form.to_dict()
        session['user_input'] = user_input
        print(user_input)
        email = request.form['email']
        session['email'] = email

        response = client.get_identity_verification_attributes(Identities=[session['email']])
        if response['VerificationAttributes']:
            verification_status = response['VerificationAttributes'][session['email']]['VerificationStatus']
            if verification_status != "Success":
                return render_template("validate_user_pending.html", email = session['email'], status = verification_status)
            else:
                return render_template("validate_user_success.html", email = session['email'], status = verification_status)
        else:
            # create identity in AWS SES
            response = client.verify_email_identity(EmailAddress=email)
    
            return render_template("validate_user_pending.html", email = session['email'], status = status)
    return render_template("validate_user_pending.html", email = session['email'], status = status)

@application.route("/verify_user_email/", )
def verify_user_email():
    email_address = session['email']
    response = client.get_identity_verification_attributes(Identities=[email_address])
    verification_status = response['VerificationAttributes'][email_address]['VerificationStatus']
    print(f"The verification status of {email_address} is {verification_status}")
    if verification_status != "Success":
        return render_template("validate_user_pending.html", email = session['email'], status = verification_status)
    elif verification_status == "Success":
        news_category = ''
        for k,v in session['user_input'].items():
            if v == '1':
                news_category += k+","
        news_category += session['user_input']['others']
        news_user = User(session['user_input']['name'],session['user_input']['email'], news_category)
        print(news_user.query.all())
        db.session.add(news_user)
        db.session.commit()
        return render_template("validate_user_success.html", email = session['email'], status = verification_status)
if __name__ == "__main__":
    application.run(host="127.0.0.1", port=8080, debug=True)