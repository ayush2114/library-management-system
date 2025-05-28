# Library Management System - V2

## Overview

The Library Management System - V2 is a multi-user application designed to facilitate the issuing, granting/revoking, and maintenance of e-books across various sections, like an online library. This project implements both backend and frontend components, offering a comprehensive solution for library management.

## Table of Contents

- [Features](#features)
- [Technology Stach](#technology-stack)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation and Running](#installation-and-running)

## Features

- User and Admin authentication with RBAC.
- Admin functionalities to create, update, and delete sections and e-books.
- User functionalities to request, read, and rate e-books.
- User can purchase and download ebook.
- Automated e-book access revocation after a set period.
- Exporting issued e-books details as CSV.
- Scheduled jobs for reminders and monthly reports using Celery and Redis.

## Technology Stack

- **Backend**: Flask, Celery
- **Frontend**: Vue.js, Bootstrap
- **Database**: SQLite
- **Caching**: Redis
- **Task-Queue**: Redis



## Prerequisites

Ensure you have the following installed on your system:

- [Go](https://golang.org/doc/install) (for MailHog)
- [Node.js](https://nodejs.org/en/download/) (v14 or later)
- [Python](https://www.python.org/downloads/) (v3.8 or later)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [Redis](https://redis.io/download) (for Celery)



## Project Structure


```
.
├── README.md                  # Project documentation
├── backend                    # Backend directory
│   ├── app.py                 # Main Flask application entry point
│   ├── application            # Application logic and configurations
│   │   ├── celery_config.py   # Celery configuration for task scheduling
│   │   ├── config.py          # General application settings
│   │   ├── create_initial_data.py # Script for initial database setup
│   │   ├── exceptions.py      # Custom exceptions
│   │   ├── extensions.py      # Flask extensions
│   │   ├── mail_service.py    # Email service configurations
│   │   ├── models.py          # Database models
│   │   ├── resources.py       # API resource classes
│   │   ├── routes.py          # Flask application routes
│   │   ├── tasks.py           # Celery tasks for background processing
│   │   └── worker.py          # Celery worker script
│   ├── requirements.txt       # Python dependencies list
│   └── user_downloads         # Directory for user download files
├── frontend                   # Frontend directory
│   ├── public                 # Public static files
│   │   └── index.html         # Main HTML file
│   ├── src                    # Source files for the Vue.js app
│   │   ├── App.vue            # Main Vue component
│   │   ├── components         # Vue components
│   │   ├── views              # Page views
│   │   ├── router             # Vue router configuration
│   │   └── store              # Vuex store for state management
│   ├── package.json           # npm package dependencies
│   └── vue.config.js          # Vue.js configuration

```

## Installation and Running

 Clone the repository:
   ```bash
   git clone https://github.com/ayush2114/library-management-system.git
   cd library-management-system
   ```
Open five terminal windows and run the following commands:

1. MailHog (for email testing):
   ```bash
   ~/go/bin/MailHog
   ```

2. Set up and run the frontend:
   ```bash
   cd frontend && npm install && npm run serve
   ```

3. Set up and run the backend:
   ```bash
   cd backend && virtualenv venv && source venv/bin/activate && pip install -r requirements.txt && python app.py
   ```

4. Celery worker:
   ```bash
   cd backend && source venv/bin/activate && celery -A app:celery_app worker -l INFO
   ```

5. Celery beat:
   ```bash
   cd backend && source venv/bin/activate && celery -A app:celery_app beat -l INFO
   ```

The application should now be running at `http://localhost:8080` (or whatever port your frontend is configured to use).

The mailhog server should also be running at `http://localhost:8025`