import unittest
import json
import tempfile
import os
from datetime import date
from app import app, db
from models import Project, Skill, ContactMessage

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE']
        app.config['TESTING'] = True
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
            project1 = Project(title="Test Project 1", description="First test project", 
                             tech_stack="Python,Flask", date_created=date(2025, 1, 1), featured=True)
            project2 = Project(title="Test Project 2", description="Second test project",
                             tech_stack="JavaScript,React", date_created=date(2025, 2, 1), featured=False)
            skill1 = Skill(name="Python", category="programming", proficiency_level=4)
            skill2 = Skill(name="Excel", category="tools", proficiency_level=3)
            db.session.add_all([project1, project2, skill1, skill2])
            db.session.commit()
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_get_all_projects(self):
        response = self.app.get('/api/projects')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertGreaterEqual(len(data['data']['projects']), 2)
    
    def test_get_featured_projects(self):
        response = self.app.get('/api/projects/featured')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['data']['projects']), 1)
        self.assertTrue(data['data']['projects'][0]['featured'])
    
    def test_get_skills(self):
        response = self.app.get('/api/skills')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('programming', data['data']['skills'])
        self.assertIn('tools', data['data']['skills'])
    
    def test_submit_contact_success(self):
        contact_data = {'name': 'John Doe', 'email': 'john@example.com', 'message': 'Test message'}
        response = self.app.post('/api/contact', data=json.dumps(contact_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
    
    def test_submit_contact_missing_fields(self):
        contact_data = {'name': 'John Doe'}
        response = self.app.post('/api/contact', data=json.dumps(contact_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')

if __name__ == '__main__':
    unittest.main()