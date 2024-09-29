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
```

## Sphinx Documentation for Django Project

This project uses **Sphinx** to generate and maintain documentation. Follow the steps below to edit the documentation and generate the HTML output.

## Editing Documentation

1. Navigate to the `docs/` folder in the project.
2. Inside the `docs/source/` folder, you will find the reStructuredText (`.rst`) files which contain the structure and content of the documentation.
3. Edit or add content to the relevant `.rst` files as needed.
   - For example, you can modify `index.rst` to update the main page or create new `.rst` files to add new sections to the documentation.

## Generating HTML Documentation

Once you've made changes to the documentation, you can generate the HTML output by running the following command:

```bash
cd docs
make html
```
