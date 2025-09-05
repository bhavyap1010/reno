# Reno

A modern Django-based platform for business profiles, service requests, and client interactions.

## 🚀 Project Overview
Reno is a web application designed to connect clients with businesses, manage service requests, and facilitate communication. It features user authentication, business listings, chat functionality, and review systems.

## 🛠️ Technologies Used
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![Django Channels](https://img.shields.io/badge/Django%20Channels-4.0-orange?logo=django)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
![WebSockets](https://img.shields.io/badge/WebSockets-Enabled-brightgreen)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)
![Zsh](https://img.shields.io/badge/Zsh-FAFAFA?logo=gnu-bash&logoColor=black)

## 🌐 Live Application

[Reno App on Render](https://reno-app.onrender.com)

## 🏗️ Features
- User registration and authentication
- Business profile management
- Service request creation and tracking
- Real-time chat between clients and businesses
- Review and rating system
- Responsive UI with custom CSS

## 📁 Folder Structure
- `client/` - Main Django app for business and client logic
  - `models.py` - Database models
  - `views.py` - View functions and classes
  - `forms.py` - Django forms
  - `consumer.py` - WebSocket consumers for chat
  - `templates/` - HTML templates
  - `static/` - CSS and images
- `server/` - Django project settings and configuration
- `media/` - Uploaded images and files

- `db.sqlite3` - SQLite database
- `manage.py` - Django management script

## ⚡️ Getting Started
1. **Clone the repository:**
	```bash
	git clone <repo-url>
	cd reno
	```
2. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```

	## 🗄️ Database
	This project uses **PostgreSQL** as the primary database. Make sure you have PostgreSQL installed and configured before running migrations.

	Update your `server/settings.py` with your PostgreSQL credentials:
	```python
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql',
			'NAME': '<your-db-name>',
			'USER': '<your-db-user>',
			'PASSWORD': '<your-db-password>',
			'HOST': 'localhost',
			'PORT': '5432',
		}
	}
	```
3. **Apply migrations:**
	```bash
	python manage.py migrate
	```
4. **Run the development server:**
	```bash
	python manage.py runserver
	```
5. **Access the app:**
	Open [http://localhost:8000](http://localhost:8000) in your browser.

## 🧪 Running Tests
```bash
python manage.py test
```

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📬 Contact
For questions or support, contact [your-email@example.com].

---
*Made with Django & ❤️*
