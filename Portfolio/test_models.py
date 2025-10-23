#!/usr/bin/env python3
"""
Unit tests for database models.
Tests model creation, validation, and serialization methods.
"""

import unittest
import tempfile
import os
from datetime import date, datetime
from app import app, db
from models import Project, Skill, ContactMessage

class TestModels(unittest.TestCase):
    """Test cases for database models"""
    
    def setUp(self):
        """Set up test database"""
        # Create temporary database file
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE']
        app.config['TESTING'] = True
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up test database"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_project_creation(self):
        """Test Project model creation and validation"""
        with app.app_context():
            project = Project(
                title="Test Project",
                description="A test project description",
                tech_stack="Python,Flask,SQLite",
                date_created=date(2025, 1, 1),
                github_url="https://github.com/test/project",
                featured=True
            )
            
            db.session.add(project)
            db.session.commit()
            
            # Test project was saved
            saved_project = Project.query.filter_by(title="Test Project").first()
            self.assertIsNotNone(saved_project)
            self.assertEqual(saved_project.title, "Test Project")
            self.assertEqual(saved_project.description, "A test project description")
            self.assertEqual(saved_project.tech_stack, "Python,Flask,SQLite")
            self.assertTrue(saved_project.featured)
            self.assertIsNotNone(saved_project.created_at)
    
    def test_project_to_dict(self):
        """Test Project model to_dict serialization"""
        with app.app_context():
            project = Project(
                title="Test Project",
                description="A test project description",
                tech_stack="Python,Flask,SQLite",
                date_created=date(2025, 1, 1),
                github_url="https://github.com/test/project"
            )
            
            db.session.add(project)
            db.session.commit()
            
            project_dict = project.to_dict()
            
            self.assertEqual(project_dict['title'], "Test Project")
            self.assertEqual(project_dict['description'], "A test project description")
            self.assertEqual(project_dict['tech_stack'], ["Python", "Flask", "SQLite"])
            self.assertEqual(project_dict['date_created'], "2025-01-01")
            self.assertEqual(project_dict['github_url'], "https://github.com/test/project")
            self.assertFalse(project_dict['featured'])  # Default value
    
    def test_skill_creation(self):
        """Test Skill model creation and validation"""
        with app.app_context():
            skill = Skill(
                name="Python",
                category="programming",
                proficiency_level=4,
                icon_class="fab fa-python"
            )
            
            db.session.add(skill)
            db.session.commit()
            
            # Test skill was saved
            saved_skill = Skill.query.filter_by(name="Python").first()
            self.assertIsNotNone(saved_skill)
            self.assertEqual(saved_skill.name, "Python")
            self.assertEqual(saved_skill.category, "programming")
            self.assertEqual(saved_skill.proficiency_level, 4)
            self.assertEqual(saved_skill.icon_class, "fab fa-python")
            self.assertIsNotNone(saved_skill.created_at)
    
    def test_skill_to_dict(self):
        """Test Skill model to_dict serialization"""
        with app.app_context():
            skill = Skill(
                name="JavaScript",
                category="programming",
                proficiency_level=3,
                icon_class="fab fa-js-square"
            )
            
            db.session.add(skill)
            db.session.commit()
            
            skill_dict = skill.to_dict()
            
            self.assertEqual(skill_dict['name'], "JavaScript")
            self.assertEqual(skill_dict['category'], "programming")
            self.assertEqual(skill_dict['proficiency_level'], 3)
            self.assertEqual(skill_dict['icon_class'], "fab fa-js-square")
    
    def test_contact_message_creation(self):
        """Test ContactMessage model creation and validation"""
        with app.app_context():
            message = ContactMessage(
                name="John Doe",
                email="john@example.com",
                subject="Test Message",
                message="This is a test message",
                ip_address="192.168.1.1"
            )
            
            db.session.add(message)
            db.session.commit()
            
            # Test message was saved
            saved_message = ContactMessage.query.filter_by(email="john@example.com").first()
            self.assertIsNotNone(saved_message)
            self.assertEqual(saved_message.name, "John Doe")
            self.assertEqual(saved_message.email, "john@example.com")
            self.assertEqual(saved_message.subject, "Test Message")
            self.assertEqual(saved_message.message, "This is a test message")
            self.assertEqual(saved_message.ip_address, "192.168.1.1")
            self.assertFalse(saved_message.read_status)  # Default value
            self.assertIsNotNone(saved_message.created_at)
    
    def test_contact_message_to_dict(self):
        """Test ContactMessage model to_dict serialization"""
        with app.app_context():
            message = ContactMessage(
                name="Jane Smith",
                email="jane@example.com",
                subject="Another Test",
                message="Another test message",
                ip_address="10.0.0.1",
                read_status=True
            )
            
            db.session.add(message)
            db.session.commit()
            
            message_dict = message.to_dict()
            
            self.assertEqual(message_dict['name'], "Jane Smith")
            self.assertEqual(message_dict['email'], "jane@example.com")
            self.assertEqual(message_dict['subject'], "Another Test")
            self.assertEqual(message_dict['message'], "Another test message")
            self.assertEqual(message_dict['ip_address'], "10.0.0.1")
            self.assertTrue(message_dict['read_status'])
    
    def test_model_repr_methods(self):
        """Test model __repr__ methods"""
        with app.app_context():
            project = Project(title="Test Project", description="Test", tech_stack="Python", date_created=date.today())
            skill = Skill(name="Python", category="programming")
            message = ContactMessage(name="John", email="john@test.com", message="Test")
            
            self.assertEqual(str(project), '<Project Test Project>')
            self.assertEqual(str(skill), '<Skill Python>')
            self.assertEqual(str(message), '<ContactMessage from John>')
    
    def test_project_tech_stack_empty(self):
        """Test Project model with empty tech_stack"""
        with app.app_context():
            project = Project(
                title="Empty Tech Stack Project",
                description="Project with no tech stack",
                tech_stack="",
                date_created=date.today()
            )
            
            db.session.add(project)
            db.session.commit()
            
            project_dict = project.to_dict()
            self.assertEqual(project_dict['tech_stack'], [])
    
    def test_skill_default_proficiency(self):
        """Test Skill model default proficiency level"""
        with app.app_context():
            skill = Skill(name="New Skill", category="learning")
            
            db.session.add(skill)
            db.session.commit()
            
            saved_skill = Skill.query.filter_by(name="New Skill").first()
            self.assertEqual(saved_skill.proficiency_level, 1)  # Default value

if __name__ == '__main__':
    unittest.main()