# Integrating Azure AD with Django

## Introduction

This documentation provides step-by-step instructions on how to integrate Azure Active Directory (Azure AD) with a Django application. Azure AD provides identity and access management for cloud applications, making it easy to secure user authentication in your Django project.

## Prerequisites

1. An Azure account.
2. A Django application.
3. Basic knowledge of Django and Azure AD.

## Step-by-Step Guide

### Step 1: Create an Azure AD App Registration

1. **Sign in to the Azure portal**: [Azure Portal](https://portal.azure.com).
2. **Navigate to Azure Active Directory**: In the left-hand navigation pane, select "Azure Active Directory".
3. **App registrations**: Under "Manage", select "App registrations", then click on "New registration".
4. **Register an application**:
    - Name: Enter a name for your application.
    - Supported account types: Select "Accounts in this organizational directory only" (Single tenant) or other options based on your requirement.
    - Redirect URI: Set the redirect URI (e.g., `http://localhost:8000/oauth2/callback` for local development).
5. **Click "Register"**.

### Step 2: Configure Authentication

1. **Platform configurations**: Under "Authentication", add a platform configuration.
    - Select "Web".
    - Add the redirect URI (same as above).
    - Enable "ID tokens" and "Access tokens".
2. **Save changes**.

### Step 3: Note Application Details

1. **Client ID**: Copy the "Application (client) ID".
2. **Tenant ID**: Copy the "Directory (tenant) ID".
3. **Client Secret**: Under "Certificates & secrets", create a new client secret and copy its value.

### Step 4: Install Required Packages

Install the required packages using pip:

```bash
pip install django-auth-adfs
```

### Step 5: Configure Django Settings

Add the following configurations to your settings.py:

# settings.py
```
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

INSTALLED_APPS = [
    ...
    'django_auth_azure_ad',
    ...
]

MIDDLEWARE = [
    ...
    'django_auth_adfs.middleware.LoginRequiredMiddleware',
    ...
]

AUTHENTICATION_BACKENDS = (
    ...
    'django_auth_adfs.backend.AdfsAuthCodeBackend',
    ...
)

ROOT_URLCONF = 'azurelogin.urls'

AZURE_AD_CLIENT_ID = 'YOUR_CLIENT_ID'
AZURE_AD_CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
AZURE_AD_TENANT_ID = 'YOUR_TENANT_ID'

LOGIN_URL = 'django_auth_adfs:login'
LOGIN_REDIRECT_URL = 'http://localhost:8000/oauth2/callback'


client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
tenant_id = os.getenv("tenant_id")


AUTH_ADFS = {
    'AUDIENCE': client_id,
    'CLIENT_ID': client_id,
    'CLIENT_SECRET': client_secret,
    'CLAIM_MAPPING': {'first_name': 'given_name',
                      'last_name': 'family_name',
                      'email': 'upn'},
    'GROUPS_CLAIM': 'roles',
    'MIRROR_GROUPS': True,
    'USERNAME_CLAIM': 'upn',
    'TENANT_ID': tenant_id,
    'RELYING_PARTY_ID': client_id,
}
```

Replace 'YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET', and 'YOUR_TENANT_ID' with the values from your Azure AD app registration.

### Step 6: Update URLs and Views
Add the Azure AD authentication views to your urls.py:


# urls.py

from django.urls import path, include
```
urlpatterns = [
    ...
    path('oauth2/', include('django_auth_adfs.urls')),
    path('', views.login_successful, name='login-view'),
    ...
]
```
### Step 7: Python-dotenv package
Install the python-dotenv package:


```bash 
pip install python-dotenv
```

### Step 8: Create .env file in main directory with app credentials
Ensure your .env file contains the necessary credentials:


```bash 
client_id=YOUR_CLIENT_ID
client_secret=YOUR_CLIENT_SECRET
tenant_id=YOUR_TENANT_ID
```

### Step 9: Create Views
Define a view in main_project_directory/views.py::


```bash 
def login_successful(request):
    return HttpResponse('login successfull')

```

### Step 10: Testing
Run the server:

```bash 
python manage.py runserver
```

Access the login URL: Navigate to http://localhost:8000/accounts/azure/login/.

Authenticate: You should be redirected to the Azure AD login page. After successful authentication, you will be redirected back to your Django application.

Troubleshooting
Invalid Client ID or Secret: Ensure that the CLIENT_ID and CLIENT_SECRET in your settings.py match those in Azure AD.
Redirect URI Mismatch: Ensure that the redirect URI in Azure AD matches the one in your settings.py.
Conclusion
By following these steps, you should have successfully integrated Azure AD with your Django application. This integration enhances your application's security by leveraging Azure AD's identity and access management capabilities.

For more detailed customization and advanced features, refer to the Django-Auth-Azure-AD documentation.