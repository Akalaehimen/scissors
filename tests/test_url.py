import unittest
from app import create_app
from api.config.config import config_dict
from utils import db
from flask.testing import FlaskClient
from unittest import TestCase
from datetime import datetime
from unittest.mock import patch
import json
from api.models.shorturl import ShortUrl
from api.models.click import Click
from api.models.user import User



class UserTestCase(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client: FlaskClient = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()




    def test_shorten_url(client):
    # test with valid long_url and domain_name
        data = {"long_url": "http://example.com", "domain_name": "example"}
        response = client.post("/shorten", json=data)
        assert response.status_code == 201
        assert "short_url" in response.json

    # test with valid long_url and empty domain_name
        data = {"long_url": "http://example.com", "domain_name": ""}
        response = client.post("/shorten", json=data)
        assert response.status_code == 201
        assert "short_url" in response.json

    # test with invalid long_url
        data = {"long_url": "not_a_valid_url", "domain_name": ""}
        response = client.post("/shorten", json=data)
        assert response.status_code == 400
        assert "Invalid URL" in response.data.decode("utf-8")

    # test with existing domain_name
        data = {"long_url": "http://example.com", "domain_name": "example"}
        response = client.post("/shorten", json=data)
        assert response.status_code == 400
        assert "Domain name already exists" in response.json["error"]



    def test_url_analytics(app, client):
    # Create a test short URL
        short_url = ShortUrl(short_url='abc123', long_url='http://example.com')
        db.session.add(short_url)
        db.session.commit()

    # Create some test clicks for the short URL
        click1 = Click(short_url_id=short_url.id, user_agent='Mozilla/5.0', referrer='http://example.com', clicked_at=datetime.now(), ip_address='127.0.0.1')
        click2 = Click(short_url_id=short_url.id, user_agent='Mozilla/5.0', referrer='http://example.com', clicked_at=datetime.now(), ip_address='127.0.0.1')
        db.session.add(click1)
        db.session.add(click2)
        db.session.commit()

    # Make a request to the url_analytics route
        response = client.get('/abc123/analytics')
        data = json.loads(response.data)

    # Check that the response contains the expected data
        assert response.status_code == 200
        assert data['short_url'] == 'abc123'
        assert data['long_url'] == 'http://example.com'
        assert data['clicks'] == 2
        assert len(data['analytics']) == 2
        assert data['analytics'][0]['user_agent'] == 'Mozilla/5.0'
        assert data['analytics'][0]['referrer'] == 'http://example.com'
        assert data['analytics'][0]['ip_address'] == '127.0.0.1'
 