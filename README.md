# LEC – Handmade Artisan Bags (Django)

A clean, modern product catalog website for LEC with WhatsApp ordering and an admin panel.

## Tech Stack
- Python 3.x
- Django (latest stable)
- SQLite for local development
- PostgreSQL-ready via `DATABASE_URL`
- Pillow for image uploads
- Bootstrap 5 via CDN
- WhiteNoise + Gunicorn for production

## Local Setup (Mac)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open: http://127.0.0.1:8000
Admin: http://127.0.0.1:8000/admin/

## Environment Variables
Set these in your shell or production dashboard:
- `SECRET_KEY` (required in production)
- `DEBUG` (True/False)
- `ALLOWED_HOSTS` (comma-separated)
- `DATABASE_URL` (PostgreSQL in production, SQLite default is used if not set)
- `WHATSAPP_NUMBER` (number only, e.g. `15551234567`)

Example:
```bash
export SECRET_KEY="change-me"
export DEBUG="False"
export ALLOWED_HOSTS="lec.com,www.lec.com"
export WHATSAPP_NUMBER="15551234567"
```

## Sample Products
Load the demo data:
```bash
python manage.py loaddata catalog/fixtures/sample_products.json
```

Note: The fixture references placeholder image paths. Upload real images in the admin panel.

## Production Notes
- Run migrations:
  ```bash
  python manage.py migrate
  ```
- Create admin user:
  ```bash
  python manage.py createsuperuser
  ```
- Collect static files:
  ```bash
  python manage.py collectstatic
  ```

## Deploy (Render)
- Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- Start command: `gunicorn lec_site.wsgi`

## Project Structure
```
lec_site/           # Django project settings
catalog/            # Main app with models, views, templates
static/             # Static assets
media/              # Uploaded product images
```
