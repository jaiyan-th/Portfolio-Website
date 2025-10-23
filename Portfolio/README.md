# Jaiyanth B - Portfolio Website

A modern, responsive portfolio website built with Flask, featuring a sleek dark theme inspired by "Bolt AI" design style.

## 🚀 Features

- **Modern Design**: Dark theme with light mode toggle
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
- **Dynamic Content**: Projects and skills loaded from SQLite database
- **Smooth Animations**: Engaging scroll-based and interactive animations
- **Accessibility**: WCAG compliant with screen reader support
- **SEO Optimized**: Meta tags, structured data, and performance optimized
- **Contact Form**: Functional contact form with validation

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, TailwindCSS, Vanilla JavaScript
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)

## 📋 Requirements

- Python 3.8+
- Flask 3.0+
- SQLAlchemy
- Modern web browser

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd portfolio-website
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python init_db.py
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   Navigate to `http://localhost`

## 🧪 Testing

Run the test suite:
```bash
# Model tests
python -m pytest test_models.py -v

# API tests
python -m pytest test_api.py -v

# All tests
python -m pytest -v
```

## 🔧 Optimization

### Performance Optimization
```bash
python optimize.py
```

### Accessibility Audit
```bash
python accessibility_audit.py
```

## 📁 Project Structure

```
portfolio-website/
├── app.py                 # Main Flask application
├── models.py             # Database models
├── init_db.py            # Database initialization
├── config.py             # Configuration settings
├── wsgi.py               # WSGI entry point
├── static/
│   ├── css/
│   │   └── styles.css    # Custom styles
│   ├── js/
│   │   ├── main.js       # Core functionality
│   │   ├── theme.js      # Theme toggle
│   │   └── animations.js # Animation controller
│   └── images/           # Static images
├── templates/
│   ├── base.html         # Base template
│   └── index.html        # Main page
├── tests/
│   ├── test_models.py    # Model tests
│   └── test_api.py       # API tests
└── deployment/
    ├── Dockerfile        # Container configuration
    ├── docker-compose.yml
    ├── nginx.conf        # Nginx configuration
    └── vercel.json       # Vercel deployment
```

## 🌐 Deployment Options

### Vercel (Recommended)
1. Install Vercel CLI: `npm i -g vercel`
2. Deploy: `vercel --prod`

### Heroku
1. Create Heroku app: `heroku create your-app-name`
2. Deploy: `git push heroku main`

### Docker
1. Build: `docker build -t portfolio .`
2. Run: `docker run -p 5000:5000 portfolio`

### Traditional Hosting
1. Upload files to server
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize database: `python init_db.py`
4. Configure web server (Apache/Nginx) to serve the Flask app

## 🎨 Customization

### Adding New Projects
1. Use the admin interface or directly add to database:
   ```python
   from models import Project
   project = Project(
       title="Your Project",
       description="Project description",
       tech_stack="Python,Flask,React",
       date_created=date.today(),
       github_url="https://github.com/username/repo",
       featured=True
   )
   db.session.add(project)
   db.session.commit()
   ```

### Modifying Styles
- Edit `static/css/styles.css` for custom styles
- Modify TailwindCSS classes in templates
- Update color scheme in CSS custom properties

### Adding New Sections
1. Add HTML structure to `templates/index.html`
2. Add corresponding JavaScript in `static/js/main.js`
3. Update navigation links in `templates/base.html`

## 📊 Performance Metrics

- **Lighthouse Score**: 95+ (Performance, Accessibility, Best Practices, SEO)
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1

## 🔒 Security Features

- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF protection
- Secure headers
- Rate limiting ready

## 📱 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Jaiyanth B**
- Email: jaiyanthofficial@gmail.com
- LinkedIn: [linkedin.com/in/jaiyanth-b-8295b2315](https://linkedin.com/in/jaiyanth-b-8295b2315)
- GitHub: [github.com/jaiyan-th](https://github.com/jaiyan-th)

## 🙏 Acknowledgments

- Design inspiration from Bolt AI
- TailwindCSS for the utility-first CSS framework
- Font Awesome for icons
- Google Fonts for typography
- Flask community for the excellent framework
