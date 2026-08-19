# Sticky Notes

A Django bulletin-board application where authors can create, view, edit, and
delete posts ("sticky notes"). Built as part of the HyperionDev Software
Engineering bootcamp (Django – Sticky Notes Application, Parts 1 & 2).

## Features

- List, view, create, update, and delete posts
- Posts are attributed to an author
- Full unit test suite covering models, views, and forms

## Design

Design diagrams (use case, class, and sequence diagrams) are in the
[`design/`](design) folder.

## Getting started

### Prerequisites

- Python 3.10+

### Setup

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/swhmcmahon/sticky_notes.git
cd sticky_notes
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Apply migrations and start the development server:

```bash
python manage.py migrate
python manage.py runserver
```

The app will be available at http://127.0.0.1:8000/.

(Optional) Create an admin user to manage posts and authors via the Django
admin site at `/admin/`:

```bash
python manage.py createsuperuser
```

## Running tests

```bash
python manage.py test posts
```

## Project structure

```
sticky_notes/
├── design/            # Use case, class, and sequence diagrams
├── posts/             # The bulletin board app (models, views, forms, tests, templates)
├── sticky_notes/       # Project settings and URL configuration
├── manage.py
└── requirements.txt
```
