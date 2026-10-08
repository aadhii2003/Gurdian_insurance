from django.urls import path, include
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

api_prefix = os.environ.get('API_PREFIX', '/api/v1').strip('/')

urlpatterns = [
    path(f'{api_prefix}/', include('apps.common.urls')),
    path(f'{api_prefix}/', include('apps.accounts.urls')),
    path(f'{api_prefix}/', include('apps.dashboard.urls')),
]
