# import os

# from flask import Flask, request, url_for
# from flask_mail import Mail, Message
# from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

# app = Flask(__name__)
# app.config[''] = '
# app.config['MAIL_PORT'] = 587
# app.config['EMAIL_TIMEOUT'] = 10
# app.config['MAIL_USE_TLS'] = 1
# app.config['MAIL_USE_SSL'] = False
# app.config.from_pyfile('config.cfg')

# mail = Mail(app)

# serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     # msg = Message("Hello", sender='daktari.weconnect@gmail.com', recipients=['dindijjames@gmail.com'])
#     # mail.send(msg)
#     # return "Message Sent!!"
#     if request.method == 'GET':
#         return '<form action="/" method="POST"><input name="email"/><input type="submit"/></form>'
#     email = request.form['email']
#     token = serializer.dumps(email, salt="email-confirmation-salt")
#     msg = Message('Confirm email', sender='daktari.weconnect@gmail.com', recipients=[email])
#     link = url_for('confirm_email', token=token, _external=True)
#     msg.body = "Your link is {}".format(link)
#     mail.send(msg)
#     return '<h3>Check your email address for an activation link to activate your email<h3>'

# @app.route('/confirm_email/<token>')
# def confirm_email(token):
#     try:
#         email = serializer.loads(token, salt="email-confirmation-salt", max_age=60)
#     except SignatureExpired:
#         return "<h3>Sorry, The token is expired!</h3>"
#     except BadTimeSignature:
#         return "<h3>Sorry, The token is not correct!</h3>"
#     return "<h3>The token works!</h3>"

# if __name__ == "__main__":
#     app.run(debug=True)