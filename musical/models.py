from django.db import models
from django.utils import timezone


class Musicals(models.Model):
    is_live = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    ticket_attribute = models.CharField(max_length=100, blank=True)
    prf_attribute = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    open_from = models.DateTimeField(default=timezone.now)
    open_to = models.DateTimeField(default=timezone.now)
    ticket_time = models.DateTimeField()
    location = models.ForeignKey('Locations', on_delete=models.CASCADE)  # 외래키 추가
    theater = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)  # 외래키 추가
    poster = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=100)
    source_id = models.IntegerField(default=1)
    cast = models.CharField(max_length=200, blank=True)
    price = models.IntegerField(default=10000)
    fail = models.BooleanField(default=False)
    fail_reason = models.CharField(max_length=200, blank=True)
    search_keyword = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Categories(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name



class Locations(models.Model):
    location_name = models.CharField(max_length=50)

    def __str__(self):
        return self.location_name
