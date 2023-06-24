from flask.views import MethodView
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required, jwt_manager)
from flask_smorest import Blueprint, abort
from flask import redirect, url_for, session
from flask_login import login_required, current_user
from utils import db
import hashlib
from api.models.user import User
from datetime import datetime
from urllib.parse import urlparse
from flask import request, jsonify, render_template
from api.models.shorturl import ShortUrl
from functools import wraps
from io import BytesIO
import qrcode
import base64
from api.models.click import Click



blp = Blueprint("Mains", "mains", description="Operations on Mains")


# Decorator function to check if the user is authenticated
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_authenticated: 
#             return redirect(url_for('Users.login_page'))  
#         return f(*args, **kwargs)
#     return decorated_function
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'user_id' not in session:
#             return redirect(url_for('Users.login_page'))
#         return f(*args, **kwargs)
#     return decorated_function


# Creating a short url and cutomization name and also validating if the url is valid
@blp.route('/shorten', methods=['POST', 'GET'])
@login_required
def shorten_url():
    if request.method == 'POST':
        long_url = request.form.get("long_url")
        domain_name = request.form.get("domain_name")
        
        try:
            validate_url(long_url)
        except ValueError as e:
            return str(e), 400
        
        # Check if the long URL has been shortened before
        url = ShortUrl.query.filter_by(long_url=long_url, domain_name=domain_name).first()
        if url:
            error_message = "URL has been shortened before, Please check your history."
            return render_template('error.html', error_message=error_message)

        hash_object = hashlib.md5(long_url.encode())
        hex_dig = hash_object.hexdigest()
        short_url = hex_dig[:4]
        new_url = ShortUrl(long_url=long_url, short_url=short_url, domain_name=domain_name)
        db.session.add(new_url)
        db.session.commit()
        
        # Construct the shortened URL
        shortened_url = f"http://127.0.0.1:5000/{domain_name}/{short_url}"

        # Generate the QR code
        qr_code_image = generate_qr_code(shortened_url)
        
        return render_template('shortenss.html', shortened_url=shortened_url, qr_code_image=qr_code_image)

    return render_template('shorten.html')

def validate_url(url):
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        raise ValueError('Invalid URL')
    
      
    
# Redirecting the user from the short link we created to the long one 
@blp.route('/<string:domain_name>/<string:short_url>')
def redirect_url(short_url, domain_name):
    url = ShortUrl.query.filter_by(short_url=short_url, domain_name=domain_name).first_or_404()
    url.clicks += 1  # increment clicks column by 1
    db.session.commit()  # save changes to the database

    # get information about the user that clicked the URL
    user_agent = request.user_agent.string
    referrer = request.referrer
    ip_address = request.remote_addr
    
    # log the click in a separate Click model
    click = Click(short_url_id=url.id, user_agent=user_agent, referrer=referrer, clicked_at=datetime.utcnow(), ip_address=ip_address)
    db.session.add(click)
    db.session.commit()

    return redirect(url.long_url)


# Getting the history of the user
@blp.route("/history", methods=["GET"])
def get_user_history():
    if not current_user.is_authenticated:
        return redirect(url_for('Users.login_page'))
    
    urls = ShortUrl.query.filter_by().all()
    if not urls:
        return render_template('history.html', error='User history not found')
    
    history = [
        {"long_url": url.long_url, "short_url": f"http://127.0.0.1:5000/{url.domain_name}/{url.short_url}", "domain_name": url.domain_name}
        for url in urls
    ]
    
    return render_template('history.html', history=history)

@blp.route("/analytics", methods=["GET"])
def url_analytics():
    urls = ShortUrl.query.all()
    analytics = []

    for url in urls:
        clicks = Click.query.filter_by(short_url_id=url.id).all()
        url_analytics = {
            "short_url": url.short_url,
            "clicks": len(clicks),
            "analytics": []
        }

        for click in clicks:
            click_info = {
                "user_agent": click.user_agent,
                "clicked_at": click.clicked_at,
                "ip_address": click.ip_address
            }
            url_analytics["analytics"].append(click_info)

        analytics.append(url_analytics)

    if not analytics:
        return render_template('error.html', error='No analytics found')

    return render_template('analytics.html', analytics=analytics)

def generate_qr_code(shortened_url):
    qr = qrcode.QRCode(version=1, box_size=6, border=2)
    qr.add_data(shortened_url)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Convert the PNG image to base64 string
    qr_image_data = BytesIO()
    qr_image.save(qr_image_data, format='PNG')
    qr_image_data.seek(0)

    qr_code_image = base64.b64encode(qr_image_data.getvalue()).decode('utf-8')

    return qr_code_image


