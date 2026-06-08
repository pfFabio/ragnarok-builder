from django.db import models

class CachedItem(models.Model):
    item_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    icon_url = models.URLField(null=True, blank=True)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    str_bonus = models.IntegerField(default=0)
    agi_bonus = models.IntegerField(default=0)
    vit_bonus = models.IntegerField(default=0)
    int_bonus = models.IntegerField(default=0)
    dex_bonus = models.IntegerField(default=0)
    luk_bonus = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item_id} - {self.name}"
