from flask import Flask, render_template, redirect
from flask.helpers import flash, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email
from mturk_unvailable import get_assin_from_str
from flask_mail import Mail, Message
import datetime
import hashlib
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message



app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess string"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "wajongichon@gmail.com"
app.config["MAIL_PASSWORD"] = "*******"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
bootstrap = Bootstrap(app)
mail = Mail(app)



#this part all about form
class ValidateForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    link = StringField("Link", validators=[DataRequired()])
    submit = SubmitField("Submit")






@app.route("/notworking", methods=['GET', 'POST'])
def notworking():
    form = ValidateForm()
    if form.validate_on_submit():
        sender_email = 'noreplay@nofaque.com'
        sender_name ='WVP'
        email = form.email.data
        link = form.link.data
        assin, region, keyword = get_assin_from_str(link)
        if assin:
            product_id = assin
          #  key_code = f"{product_id}{datetime.now(tz=timezone.utc).strftime('%Y-%m-%d')}"
          #  code = hash_md5(key_code)[10:-10]
            key_code = product_id
            code = hashlib.md5(key_code.encode()).hexdigest()
            send_email(email, "Validate with ths", 'mail/valid', code=code)
            flash("Your code already send to your email")
            return redirect(url_for('notworking'))
        else:
            send_email(email, "Not Valid bro", 'mail/notvalid')
            flash("your link not correct check again")
            return redirect(url_for('notworking'))

    return render_template("validateform.html", form=form)



def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
#    app = current_app.get_current_object()
    msg = Message(subject=subject, sender='wajongichon@gmail.com', recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr






if __name__ == "__main__":
    app.run(debug=True)

