#!/usr/bin/env python3
"""
Database initialization script for the portfolio website.
Creates tables and populates initial data for Jaiyanth B's portfolio.
"""

from app import app
from models import db, Project, Skill, ContactMessage
from datetime import date

def init_database():
    """Initialize database with tables and sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created successfully")
        
        # Clear existing data (for fresh start)
        db.session.query(Project).delete()
        db.session.query(Skill).delete()
        db.session.query(ContactMessage).delete()
        
        # Add sample projects for Jaiyanth B
        projects = [
            Project(
                title="Fake News Detection Web App",
                description="A machine learning-powered web application that analyzes news articles and determines their authenticity using advanced NLP techniques and scikit-learn algorithms. Features real-time analysis, confidence scoring, and detailed explanations of detection criteria.",
                tech_stack="Flask,Python,Scikit-learn,MongoDB,HTML,CSS,JavaScript",
                date_created=date(2025, 8, 15),
                github_url="https://github.com/jaiyan-th/fake-news-detector",
                demo_url=None,
                image_url="/static/images/fake-news-project.jpg",
                featured=True
            ),
            Project(
                title="SecureDesk - Notes & Password Manager",
                description="A comprehensive desktop application for secure note-taking and password management. Features AES encryption, secure password generation, organized categorization, and cross-platform compatibility with a clean, intuitive interface.",
                tech_stack="Flask,HTML,CSS,JavaScript,SQLite,Encryption",
                date_created=date(2025, 10, 20),
                github_url="https://github.com/jaiyan-th/securedesk",
                demo_url=None,
                image_url="/static/images/securedesk-project.jpg",
                featured=True
            )
        ]
        
        # Add programming skills
        programming_skills = [
            Skill(name="Python", category="programming", proficiency_level=4, icon_class="fab fa-python"),
            Skill(name="HTML/CSS", category="programming", proficiency_level=4, icon_class="fab fa-html5"),
            Skill(name="JavaScript", category="programming", proficiency_level=3, icon_class="fab fa-js-square"),
            Skill(name="Java (Basics)", category="programming", proficiency_level=2, icon_class="fab fa-java"),
        ]
        
        # Add tools
        tools = [
            Skill(name="Excel", category="tools", proficiency_level=4, icon_class="fas fa-file-excel"),
            Skill(name="Word", category="tools", proficiency_level=4, icon_class="fas fa-file-word"),
            Skill(name="Canva", category="tools", proficiency_level=3, icon_class="fas fa-palette"),
            Skill(name="AI Studio", category="tools", proficiency_level=3, icon_class="fas fa-robot"),
        ]
        
        # Add learning areas
        learning_skills = [
            Skill(name="SQL", category="learning", proficiency_level=2, icon_class="fas fa-database"),
            Skill(name="AI Tools", category="learning", proficiency_level=2, icon_class="fas fa-brain"),
            Skill(name="Full-Stack Development", category="learning", proficiency_level=2, icon_class="fas fa-code"),
        ]
        
        # Add all data to session
        for project in projects:
            db.session.add(project)
        
        for skill in programming_skills + tools + learning_skills:
            db.session.add(skill)
        
        # Commit all changes
        try:
            db.session.commit()
            print("✓ Sample data added successfully")
            print(f"  - Added {len(projects)} projects")
            print(f"  - Added {len(programming_skills)} programming skills")
            print(f"  - Added {len(tools)} tools")
            print(f"  - Added {len(learning_skills)} learning areas")
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error adding sample data: {e}")
            raise

def reset_database():
    """Reset database by dropping and recreating all tables"""
    with app.app_context():
        db.drop_all()
        print("✓ Database tables dropped")
        init_database()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        init_database()
    
    print("✓ Database initialization complete!")