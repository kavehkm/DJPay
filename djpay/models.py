# dj
from django.db import models


class Bill(models.Model):
    """Bill"""

    backend = models.CharField(max_length=150)
    amount = models.PositiveBigIntegerField()
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    extra = models.JSONField(default=dict)
    next_step = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def has_next_step(self):
        return True if self.next_step else False

    def __str__(self):
        return f"{self.backend}-{self.id}"

    def __repr__(self):
        return f"Bill(id={self.id}, backend={self.backend})"
