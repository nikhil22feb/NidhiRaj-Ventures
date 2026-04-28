import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# 🔥 AUTO MIGRATE (IMPORTANT)
from django.core.management import call_command
try:
    call_command('migrate', interactive=False)
    call_command('collectstatic', interactive=False)
except Exception as e:
    print("Migration error:", e)

application = get_wsgi_application()