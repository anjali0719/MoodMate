# MoodMate

[![GitHub Repository](https://img.shields.io/badge/github-MoodMate-blue?style=flat&logo=github)](https://github.com/anjali0719/MoodMate)

## Prerequisites

- Python 3.10 or higher (using Python 3.13.5)
- PostgreSQL (using PostgreSQL 17)
- Any Database Client (recommended - pgAdmin / Dbeaver)
- OpenAI Account
- Typesense Account


## Installation

### Clone the Repo

```bash
git clone https://github.com/anjali0719/MoodMate
cd MoodMate
```

### Setting up the Virtual Env.

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/MacOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Env File.
#### All the configs are based upon env keys, so make sure you've them setup beforehand. Take a look of what all things are required

```ini
OPENAI_API_KEY=value
TYPESENSE_ADMIN_API_KEY=value
TYPESENSE_SEARCH_API_KEY=value
TYPESENSE_HOST=value
TYPESENSE_PORT=value
TYPESENSE_PROTOCOL=value
DB_NAME=value
DB_USER=value
DB_PASSWORD=value
DB_HOST=value
DB_PORT=value
```

### Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### Run Development Server
```bash
python manage.py runserver
```
