import unittest
from app import create_app
from api.config.config import config_dict
from utils import db
from api.models.user import User
from werkzeug.security import generate_password_hash
from flask.testing import FlaskClient
import pytest



@pytest.fixture
def client() -> FlaskClient:
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

class UserTestCase(unittest.TestCase):
    
    def setUp(self):

        self.app = create_app(config=config_dict['test'])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()


    def tearDown(self):

        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None


    def test_user_registration(self):

        data = {
            "username": "Test",
            "email": "testuser@gmail.com",
            "password": "password",
            "confirm_password": "password"
        }

        response = self.client.post('/register', json=data)


        user = User.query.filter_by(email='testuser@gmail.com').first()

        assert user.username == "Test"

        assert response.status_code == 201


    def test_user_login(self):
        data = {
            "email":"testuser@gmail.com",
            "password": "password"
        }
        response = self.client.post('/login', json=data)

   
        assert response.status_code == 401


    # def test_delete_user(client, auth):
    # # create a test user
    #     User.register("test_user", "test_password")
    
    # # log in the test user
    #     User.login("test_user", "test_password")
    
    # # send a DELETE request to delete the user
    # response = client.delete("/users/test_user")
    
    # # assert that the response status code is 200
    # assert response.status_code == 200
    
    # # assert that the response contains the message "User deleted successfully"
    # assert b"User deleted successfully" in response.data
    
    # # assert that the user has been deleted from the database
    # assert User.query.filter_by(username="test_user").first() is None