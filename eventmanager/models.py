"""
Definition of event model.
"""
import uuid
from django.db import models
from django.utils import timezone


class Event(models.Model):
    """
    Representation of an event that occured in the system.
    Attributes:
    name(str): The name of the event.
    uuid(uuid): Unique identifier of the event, it is automatically generated on event creation.
    source(str): Source of event.
    created_at(datetime): Date and time when event was created.
    updated_at(datetime): Date and time when event was updated.
    description(str): just description of an event.
    """
    SOURCES = (
        ("users", "users"),
        ("products", "products"),
    )

    name = models.CharField(max_length=50, blank=False, null=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=50, choices=SOURCES)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField(max_length=155, blank=False, null=False)

    def save(self, *args, **kwargs):
        """
        Overriding the default save method, now when the event is updated it will generate
        updated_at.
        """
        if not self.pk:
            self.updated_at = None
        else:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)
