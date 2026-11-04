# PHILEX MEDIA FINANCIAL

A standalone Django web application and installable Progressive Web App starter.
It is separate from any other Philex Media project.

## Current scope
- Account registration and login
- Owner dashboard
- Owner capital, business income and expense records
- Basic financial totals and reports
- Responsive layout for computers, phones and tablets
- PWA manifest and service worker

## Important limitations
This starter is a financial recordkeeping demonstration only. It does not accept deposits,
hold customer funds, process payments, provide investment products, pool money, calculate
promised returns, or provide regulated financial services. Records are user-entered and are
not bank balances or audited accounts. Do not enter sensitive banking credentials.

Before any public-money or investment feature is considered, obtain qualified legal advice
and all applicable authorisations in the relevant jurisdiction. Do not enable such features
by simply adding a payment button.

## Run locally in Termux / Linux / macOS / Windows
1. Install Python 3.11+.
2. In this folder run:
   `python -m venv .venv`
3. Activate the environment:
   - Linux/macOS/Termux: `source .venv/bin/activate`
   - Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
4. Install dependencies:
   `pip install -r requirements.txt`
5. Create database tables:
   `python manage.py migrate`
6. Create an administrator account:
   `python manage.py createsuperuser`
7. Start:
   `python manage.py runserver 0.0.0.0:8000`
8. Open `http://127.0.0.1:8000` on the same device.

## Before deployment
- Set a unique, secret DJANGO_SECRET_KEY.
- Set DJANGO_DEBUG=0.
- Set DJANGO_ALLOWED_HOSTS to your real hostnames.
- Configure PostgreSQL and HTTPS.
- Configure secure cookies, backups, monitoring, and an appropriate privacy notice.
- The domain `financial.philexmedia.com` is a preferred address only; it is not registered or connected by this starter. You need control of the parent domain and hosting/DNS access to point it to a deployment.
- Test the service worker and installation on actual target devices.
