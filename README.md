# django-rest-cookiecutter

# Admin

This project integrates the **Unfold** admin interface to enhance the admin experience. The following instructions explain how to properly set up  Django admin by extending the custom `ModelAdmin` provided by Unfold.


## Setup

To ensure that the admin classes are properly configured to work with **Unfold**, follow these steps:

### Step 1: Inherit from Unfold's `ModelAdmin`

Update your admin classes to inherit from `unfold.admin.ModelAdmin` instead of Django's default `ModelAdmin`.

**Example:**

```python
# admin.py

from django.contrib import admin
from unfold.admin import ModelAdmin

@admin.register(MyModel)
class CustomAdminClass(ModelAdmin):
    pass
```

### Step 2: Handle Third-Party Admin Models
Third-party packages that register admin models using django.contrib.admin.ModelAdmin will not work properly with Unfold. You must unregister these models and re-register them using unfold.admin.ModelAdmin.

Example:
```python

# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.admin import ModelAdmin

# Unregister the existing User and Group models
admin.site.unregister(User)
admin.site.unregister(Group)

# Re-register them with Unfold's ModelAdmin
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
```

## Dynamic Model Registration

The project dynamically loads and registers all models from all installed apps using Unfold's `ModelAdmin`. No manual registration is required for each model.

# Django Application Metrics

This Django application is configured to export its statistics. 
metrics are accessible at `http://127.0.0.1:8000/metrics`.

# Django Application Health Checks

This Django application includes health check endpoints to monitor its status. You can view the application's health by accessing the following URL:

## Health Check URL
- **Endpoint:** `/health`

Visit this endpoint to see the current health status of the project. It will return a response indicating whether the application is operational.

## Example Response
```json
{
  "status": "ok"
}
