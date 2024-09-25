from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.apps import apps

from unfold.admin import ModelAdmin


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


# Loop through all installed apps and get their models
for app_config in apps.get_app_configs():
    app_models = app_config.get_models()

    for model in app_models:
        try:
            attrs = {
                "list_display": [
                    f.name
                    for f in model._meta.get_fields()
                    if not f.many_to_many and not f.one_to_many
                ]
            }
            name = "Admin_" + model.__name__
            theclass = type(str(name), (ModelAdmin,), attrs)
            admin.site.register(model, theclass)
        except AlreadyRegistered:
            pass
