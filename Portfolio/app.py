from flask import Flask, render_template, jsonify, request
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and models
from models import db, Project, Skill, ContactMessage
db.init_app(app)

@app.route('/')
def index():
    """Main portfolio page"""
    return render_template('index.html')

@app.route('/api/projects')
def get_projects():
    """API endpoint to get all projects"""
    try:
        projects = Project.query.all()
        projects_data = []
        for project in projects:
            projects_data.append({
                'id': project.id,
                'title': project.title,
                'description': project.description,
                'tech_stack': project.tech_stack.split(',') if project.tech_stack else [],
                'date_created': project.date_created.strftime('%Y-%m-%d') if project.date_created else None,
                'github_url': project.github_url,
                'demo_url': project.demo_url,
                'featured': project.featured
            })
        
        return jsonify({
            'status': 'success',
            'data': {'projects': projects_data},
            'message': 'Projects retrieved successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': {
                'code': 'DATABASE_ERROR',
                'message': 'Failed to retrieve projects'
            }
        }), 500

@app.route('/api/projects/featured')
def get_featured_projects():
    """API endpoint to get featured projects only"""
    try:
        projects = Project.query.filter_by(featured=True).all()
        projects_data = []
        for project in projects:
            projects_data.append({
                'id': project.id,
                'title': project.title,
                'description': project.description,
                'tech_stack': project.tech_stack.split(',') if project.tech_stack else [],
                'date_created': project.date_created.strftime('%Y-%m-%d') if project.date_created else None,
                'github_url': project.github_url,
                'demo_url': project.demo_url,
                'featured': project.featured
            })
        
        return jsonify({
            'status': 'success',
            'data': {'projects': projects_data},
            'message': 'Featured projects retrieved successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': {
                'code': 'DATABASE_ERROR',
                'message': 'Failed to retrieve featured projects'
            }
        }), 500

@app.route('/api/skills')
def get_skills():
    """API endpoint to get all skills grouped by category"""
    try:
        skills = Skill.query.all()
        skills_by_category = {}
        
        for skill in skills:
            category = skill.category
            if category not in skills_by_category:
                skills_by_category[category] = []
            
            skills_by_category[category].append({
                'id': skill.id,
                'name': skill.name,
                'proficiency_level': skill.proficiency_level,
                'icon_class': skill.icon_class
            })
        
        return jsonify({
            'status': 'success',
            'data': {'skills': skills_by_category},
            'message': 'Skills retrieved successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': {
                'code': 'DATABASE_ERROR',
                'message': 'Failed to retrieve skills'
            }
        }), 500

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """API endpoint to handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('name') or not data.get('email') or not data.get('message'):
            return jsonify({
                'status': 'error',
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Name, email, and message are required fields'
                }
            }), 400
        
        # Create new contact message
        contact_message = ContactMessage(
            name=data['name'],
            email=data['email'],
            subject=data.get('subject', ''),
            message=data['message'],
            ip_address=request.remote_addr
        )
        
        db.session.add(contact_message)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Message sent successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'error': {
                'code': 'DATABASE_ERROR',
                'message': 'Failed to send message'
            }
        }), 500

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)