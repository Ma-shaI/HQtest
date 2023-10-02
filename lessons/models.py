from django.contrib.auth.models import User
from django.db import models
from products.models import Product


class Lesson(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField()
    duration = models.IntegerField()
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']


class LessonViewed(models.Model):
    DoesNotExist = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewing_time = models.IntegerField()
    date = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.lesson}: {self.status}'

    def mark_viewed(self):
        percent = (int(self.viewing_time) / int(self.lesson.duration)) * 100
        if percent >= 80:
            self.status = True
            self.save()

