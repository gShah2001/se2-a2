import os, tempfile, pytest, logging, unittest
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash



from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    apply_to_job, 
    create_job
)

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass", "bob@email.com", "321-1234", "user") 
        assert user.name == "bob"  

    def test_get_json(self):
        user = User("bob", "bobpass", "bob@email.com", "321-1234", "user")  
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id": None, "name": "bob", "role": "user"})  

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", "bobpass", "bob@email.com", "321-1234", "user")  
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password, "bob@email.com", "321-1234", "user")  
        assert user.check_password(password)


'''
    Integration Tests
    #notpassing
'''

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass", "bob@email.com", "321-1234", "user")
    assert login("bob", "bobpass") != None


class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("bob", "bobpass", "bob@email.com", "321-1234", "user")
        assert user.name == "bob"

    
    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob", "role":"user"}], users_json)
        #self.assertListEqual([{"id":1, "username":"bob", "role":"user"}, {"id":2, "username":"jane", "role":"user"}], users_json)

   

class JobsIntegrationTests(unittest.TestCase):

    def test_create_job(self):
        job = create_job("Software Engineer", "Develop and maintain software", "TechCorp")
        assert job.title == "Software Engineer"

    def test_get_all_jobs_json():
        jobs_json = get_all_jobs_json()
        self.assertListEqual([
            {'id': 1, 'title': 'Software Engineer', 'description': 'Develop and maintain software.', 'company': 'TechCorp'},
            {'id': 2, 'title': 'Marketing Manager', 'description': 'Lead marketing campaigns and strategies.', 'company': 'MarketingPro'}
        ], jobs_json)

    def test_apply_to_job(self):
        apply_to_job(1, 1)
        applications = get_all_applications_json(1)
        self.assertIn({"user_id": 1, "job_id": 1}, applications)

    def test_get_all_applications_json(self):
        applications_json = get_all_applications_json(1)
        expected_applications = [{"user_id": 1, "job_id": 1}, {"user_id": 2, "job_id": 1}]
        self.assertListEqual(expected_applications, applications_json)