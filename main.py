
# A very simple Flask Hello World app for you to get started with...
import os
import random
import requests

from flask import Flask, render_template, url_for, request, redirect

from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME = os.environ.get('email_gmail'),
    MAIL_PASSWORD = os.environ.get('password_gmail')
)
mail = Mail(app)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# @app.route('/en_construction')
# def hello_world():
#     return render_template('comingsoon.html')

@app.route('/')
@app.route('/index')
@app.route('/mariage')
def index():
    path_portfolios = os.path.join(BASE_DIR, 'static', 'portfolios')
    elements_in_portfolios = os.listdir(path_portfolios)
    list_name_img = [name_img for name_img in elements_in_portfolios
                     if os.path.isfile(os.path.join(path_portfolios, name_img))]
    paths = [url_for('static', filename=os.path.join('portfolios', name_img)) for name_img in list_name_img]
    results = []
    for path, name in zip(paths, list_name_img):
        # FIXME: plusieurs catégories possible pour une même photo
        if 'business' in name:
            results.append({'url': path, 'category': 'business'})
        elif 'event' in name:
            results.append({'url': path, 'category': 'event'})
        elif 'clip' in name:
            results.append({'url': path, 'category': 'clip'})
        elif 'mariage' in name:
            results.append({'url': path, 'category': 'mariage'})
        else:
            results.append({'url': path, 'category': 'autre'})
    
    random.shuffle(results)

    path_partenaires = os.path.join(BASE_DIR, 'static', 'logo_partenaires')
    elements_in_partenaires = os.listdir(path_partenaires)
    list_name_img = [name_img for name_img in elements_in_partenaires
                     if os.path.isfile(os.path.join(path_partenaires, name_img))]
    paths = [url_for('static', filename=os.path.join('logo_partenaires', name_img)) for name_img in list_name_img]
    random.shuffle(paths)

    # paths contains: [url_for(...portfolios/xxx), url_for(...portfolios/yyy), ...]
    return render_template('index.html', images_portfolios=results, logo_partenaires=paths)

@app.route('/contact', methods=['POST'])
def contact():
    apikey_mailgun = os.environ.get("apikey_mailgun")
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')

    requests.post("https://api.mailgun.net/v3/mail.4-you.fr/messages",
                    auth=("api", apikey_mailgun),
                    data={"from": f"{name} <{email}>",
                            "to": "ismael.fr@hotmail.fr",
                            "bcc": "xuan.polinfo@gmail.com",
                            "subject": "Message à partir du site web de 4-you.fr",
                            "text": f"Email: {email}\nPhone: {phone}\n{message}"})

    # from flask_mail import Message
    # msg = Message("Message à partir du site web de 4-you.fr", recipients=['xuan.polinfo@gmail.com'])
    # msg.body = f"Email: {email}\nPhone: {phone}\n{message}"
    # mail.send(msg)


    return redirect(url_for('index'))
