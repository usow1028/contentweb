# AI vs Human Platform

This repository contains the Django REST API and React front-end for the AI vs Human blind testing competition platform.

## Backend (Django)

### Setup
1. Create a virtual environment and install dependencies:
   ```bash
   pip install django djangorestframework
   ```
2. Apply migrations and create a superuser:
   ```bash
   python backend/manage.py migrate
   python backend/manage.py createsuperuser
   ```
3. Run the development server:
   ```bash
   python backend/manage.py runserver
   ```

### Weekly Results Command
Run the custom management command to compute weekly rankings and points:
```bash
python backend/manage.py compute_weekly_results
```

## Frontend (React)

### Setup
1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server:
   ```bash
   npm start
   ```

The front-end expects the Django API to be available at `/api/`.
