#  AuthLib / OAuth2 Integration in Django with django-oauth-toolkit

This guide documents the full process of configuring OAuth2 authentication using `django-oauth-toolkit` for the **Cheaper backend**.

---

## 📦 Step 1: Install django-oauth-toolkit

```bash
pip install django-oauth-toolkit
```

---

## ⚙️ Step 2: Add to `INSTALLED_APPS`

In `cheaper/settings.py`, added:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'oauth2_provider', added 
]
```

---

## 🔐 Step 3: Add OAuth2 backend

Still in `settings.py`:

```python
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',    
    'oauth2_provider.backends.OAuth2Backend',
)
```

---

## 🌐 Step 4: Add OAuth2 URLs

In `cheaper/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include  # ✅ include added here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
```

---

## 🧱 Step 5: Run Migrations

```bash
python manage.py migrate
```

You should see migrations for `oauth2_provider` applying successfully.

---

## 👤 Step 6: Create Superuser

```bash
python manage.py createsuperuser
```

Then visit:
```
http://127.0.0.1:8000/admin
```

Login and go to **"Applications"** → Add:
- Client Type: Confidential
- Grant Type: Resource owner password-based
- Fill in user and redirect URI (can be `http://localhost`)

---

## 🔁 Step 7: Test OAuth2 Token Endpoint

### POST `/o/token/`
Send via Postman or frontend:

```x-www-form-urlencoded
grant_type: password
username: user@example.com
password: password123
client_id: your-client-id
client_secret: your-client-secret
```

### Example Response:
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "Bearer",
  "expires_in": 36000,
  "scope": "read write"
}
```

---

## ✅ Git & PR Instructions

```bash
git checkout -b setup-django-oauth
git add .
git commit -m "Configure OAuth2 using django-oauth-toolkit (#32)"
git push origin setup-django-oauth
```

Then open a pull request from `forzman/setup-django-oauth` → `James-Cheaper/main`, and reference **Issue #32**.

---

## 🚀 Next Steps
- [ ] Create custom `/register` API
- [ ] Connect frontend login form to `/o/token/`
- [ ] Secure protected views using `@protected_resource` or DRF permissions

---

> Maintained by: Abraham Forson
> Issue Ref: #32
> Backend Auth using: `django-oauth-toolkit`
