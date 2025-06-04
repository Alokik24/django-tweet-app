
# Django Tweet App

A practice Django-based backend application designed for experimenting with social media-like features such as user-generated content and tweet management.

##  Features

- User authentication (sign up, login, logout)
- Create, read, update, and delete tweets
- SQLite as the default database
- Admin panel for backend management
- RESTful architecture (if applicable)
- Deployable on platforms like Heroku or Render

##  Tech Stack

- **Backend Framework**: Django (Python)
- **Database**: SQLite (default)
- **Deployment**: Procfile and `render.yaml` support
- **Version Control**: Git

##  Setup Instructions (Local)

### 1. Clone the Repository

```bash
git clone https://github.com/Alokik24/django-tweet-app.git
cd django-tweet-app
```

### 2. Create Virtual Environment and Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 5. Run the Server

```bash
python manage.py runserver
```

## License

This project is for educational purposes and does not include a specific license.
