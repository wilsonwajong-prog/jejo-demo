from flask import Flask, render_template
from flask.helpers import flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email
from mturk_unvailable import get_assin_from_str
from helpers_csm import hash_md5, ago_from_timetime
from helpers_email import send_email_ses

app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess string"
bootstrap = Bootstrap(app)


#this part all about form
class ValidateForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    link = StringField("Link", validators=[DataRequired()])
    submit = SubmitField("Submit")






@app.route("/notworking")
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
            key_code = f"{product_id}{datetime.now(tz=timezone.utc).strftime('%Y-%m-%d')}"
            code = hash_md5(key_code)[10:-10]
            msg_body_html = f"""\
                <html><body>
                Thanks for reporting an unavailable product. Please enter the following code at every Answer field and submit the HIT and the HIT should be approved:<br>
                {code}<br><br>
                Please don't reply to this email as it's fully automated.<br>
                Please note that the code is valid for 3 hours.<br>
                Thanks again for your efforts and good luck on MTurk!
                </body></html>
                """
            msg_body_text = f"""\
                Thanks for reporting an unavailable product. Please enter the following code at every Answer field and submit the HIT and the HIT should be approved:
                {code}

                Please don't reply to this email as it's fully automated.
                Please note that the code is valid for 3 hours.
                Thanks again for your efforts and good luck on MTurk!
                """
            send_email_ses(email, "Here's your code", msg_body_html, msg_body_text, sender=sender_email, sender_name=sender_name)
            flash("Your code already send to your email")
        else:
            msg_body_html = f"""\
                <html><body>
                I'm afraid that we couldn't get the information that we need to generate an approval code from your email.<br>
                Please check that you've emailed the exact complete link in HIT step 1) that should look like 'https://../../..' (right click and copy the link; opening it and copying the link from your browser address bar might not work)<br>
                This process is fully automated so anything else you mention in the mail won't taken notice of.<br><br>
                We appreciate your work on our HIT's, but unfortunately we also encounter a lot of automated submissions. Please note that we take reporting products as unavailable while they are available to save time on completing our HIT's very seriously. We manually check reports and if we notice suspicious patterns we'll manually reject the associated assignment and block your worker account.<br><br>
                </body></html>
                """
            msg_body_text = f"""\
                I'm afraid that we couldn't get the information that we need to generate an approval code from your email.
                Please check that you've emailed the exact complete link in HIT step 1) that should look like 'https://../../..' (right click and copy the link; opening it and copying the link from your browser address bar might not work).
                This process is fully automated so anything else you mention in the mail won't taken notice of.

                We appreciate your work on our HIT's, but unfortunately we also encounter a lot of automated submissions. Please note that we take reporting products as unavailable while they are available to save time on completing our HIT's very seriously. We manually check reports and if we notice suspicious patterns we'll manually reject the associated assignment and block your worker account.
                """
            send_email_ses(email, "Validation failed", msg_body_html, msg_body_text, sender=sender_email, sender_name=sender_name)
            flash("your link not correct check again")

    return render_template("validateform.html", form=form)









if __name__ == "__main__":
    app.run(debug=True)

