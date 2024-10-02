
# django-rest-cookiecutter
### Features

This Django project includes several integrated features that enhance functionality, monitoring, and configuration flexibility.

### 1. Unfold Admin

**Feature**: Auto-add models to the Django admin using Unfold Admin for an enhanced UI and extra tools.

- Provides improved filters, forms, and inline views.
- Adds import/export functionality for models automatically.

### 2. Prometheus Metrics
### 3. Docker Support
### 4. DRF (Django REST Framework)
### 5. Sphinx Docs with Sidecar
### 6. Logging
### 7. Split Settings
### 8. Python Decouple

---
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

# Django Abstract Models: Timestamped & Non-Deletable

This project includes two reusable abstract models designed for managing time-based data and handling record deletions securely. Both models are ordered by `id` by default and can be easily extended to fit your needs.

## 1. TimeStampedModel

### Description:
The `TimeStampedModel` provides automatic tracking of record creation and updates. It includes two fields:
- **created_at**: Automatically stores the date and time when the object is first created.
- **updated_at**: Automatically updates every time the object is modified.

### Usage:
Inherit from `TimeStampedModel` in any model where you want to track the creation and modification times of your records. These fields are added automatically and require no additional configuration.

## 3. NonDeletableModel

### Description:
The `NonDeletableModel` provides a mechanism to prevent hard deletion of records from the database. Instead of allowing direct deletion, it supports "soft deletion" by marking records as deleted via a `deleted_at` field, and provides methods for restoring soft-deleted records.

### Features:
- **soft_delete()**: Marks the object as deleted by setting the `deleted_at` timestamp.
- **restore()**: Restores the object by removing the `deleted_at` timestamp.
- **is_deleted**: Property that checks whether the object has been soft-deleted.
- **Prevents hard deletion**: Direct use of `.delete()` raises an exception, ensuring that data is not permanently deleted.

### Usage:
Inherit from `NonDeletableModel` in any model where you want to implement soft deletion. This can be useful in cases where data integrity is important, and you want to avoid accidental loss of records.
 n