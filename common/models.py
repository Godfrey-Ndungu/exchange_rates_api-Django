from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['id']

    def save(self, *args, **kwargs):
        """Override save method to update timestamp"""
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class NonDeletableModel(TimeStampedModel):
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['id']

    def delete(self, *args, **kwargs):
        # Prevent hard deletion
        raise NotImplementedError(
            "Direct deletion is not allowed. Use soft_delete() instead.")

    def soft_delete(self):
        """Mark the object as deleted by setting deleted_at"""
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restore a soft-deleted object"""
        self.deleted_at = None
        self.save()

    @property
    def is_deleted(self):
        return self.deleted_at is not None
