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

class PushNotification(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    push_at = models.DateTimeField(blank=True, null=True)

class MusicalSeries(models.Model):
    series_name = models.CharField(max_length=50)
    series_description = models.TextField()
    ticket_time = models.DateTimeField()
    musical_id = models.ForeignKey('Musicals', on_delete=models.CASCADE)
    cast = models.CharField(max_length=200, blank=True)
    reservation_source = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.musical_id.title +" - " + self.series_name

class MusicalSource(models.Model):
    source_name = models.CharField(max_length=50)
    source_link = models.CharField(max_length=50)

    def __str__(self):
        return self.source_name

class MusicalReservationLink(models.Model):
    reservation_link = models.CharField(max_length=100)
    series_id = models.ForeignKey('MusicalSeries', on_delete=models.CASCADE)
    source_id = models.ForeignKey('MusicalSource', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.series_id.series_name} - {self.source_id.source_name}'

class Categories(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class TicketNotification(models.Model):
    musical_id = models.ForeignKey('Musicals', on_delete=models.CASCADE)
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
    is_notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.musical_id.title

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

class Users(models.Model):
    user_id = models.CharField(max_length=50)
    user_email = models.EmailField()
    user_password = models.CharField(max_length=50)
    user_phone = models.CharField(max_length=50)
    user_address = models.CharField(max_length=100)
    user_nickname = models.CharField(max_length=50)
    user_last_login = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user_id + " - " + self.user_last_login.strftime('%Y-%m-%d %H:%M:%S')