import json
import uuid

from django.db import models
from django.utils import timezone

from documents.models import Website


class ScrapyItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unique_id = models.CharField(max_length=100, null=True)
    data = models.TextField()  # this stands for our crawled data
    date = models.DateTimeField(default=timezone.now)

    website = models.ForeignKey(
        Website,
        related_name="scrapy_item_website",
        on_delete=models.CASCADE,
    )

    # This is for basic and custom serialisation to return it to client as a JSON.
    @property
    def to_dict(self):
        data = {
            'data': json.loads(self.data),
            'date': self.date
        }
        return data

    def __str__(self):
        return self.unique_id
