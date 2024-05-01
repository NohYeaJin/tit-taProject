from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django_quill.fields import QuillField

class Musicals(models.Model):
    is_live = models.BooleanField(default=False)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)  # 외래키 추가
    title = models.CharField(max_length=100)
    ticket_attribute = models.CharField(max_length=100, blank=True)
    prf_attribute = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    open_from = models.DateTimeField(default=timezone.now)
    open_to = models.DateTimeField(default=timezone.now)
    ticket_time = models.DateTimeField()
    location = models.ForeignKey('Locations', on_delete=models.CASCADE)  # 외래키 추가
    theater = models.CharField(max_length=100, blank=True)
    genre = models.ForeignKey('Genres', on_delete=models.CASCADE)  # 외래키 추가
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

    def img_preview(self):
        return mark_safe('<img src = "{url}" width = "300"/>'.format(url=self.poster))

class Categories(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Locations(models.Model):
    location_name = models.CharField(max_length=50)

    def __str__(self):
        return self.location_name

class Genres(models.Model):
    genre_name = models.CharField(max_length=50, default='')
    def __str__(self):
        return self.genre_name

class MainImages(models.Model):
    image_url = models.CharField(max_length=100)
    sequence = models.IntegerField(unique=True, choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return str(self.sequence) + " " + self.image_url

    def img_preview(self):
        return mark_safe('<img src = "{url}" width = "300"/>'.format(url=self.image_url))

class Notice(models.Model):
    notice_title = models.CharField(max_length=100)
    notice_content = QuillField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.notice_title