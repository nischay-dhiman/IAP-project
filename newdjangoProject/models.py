import decimal

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from newdjangoProject.validators import validate_price

DISCOUNT_PERCENT = 10

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return 'Name=' + self.name + ' Category=' + self.category

    def get_category(self):
        return self.category


class Course(models.Model):
    topic = models.ForeignKey(
        Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[validate_price])
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)
    stages = models.PositiveIntegerField(default=3)

    def __str__(self):
        return 'Topic=' + self.topic.name + ' Name=' + self.name + ' Price=' + str(self.price) + ' For everyone=' + str(
            self.for_everyone)

    def discount(self):
        discount = str(
            round(self.price-(self.price * decimal.Decimal(DISCOUNT_PERCENT/100)), 2))
        return discount


class Student(User):
    CITY_CHOICES = [
        ('WS', 'Windsor'),
        ('CG', 'Calgery'),
        ('MR', 'Montreal'),
        ('VC', 'Vancouver')
    ]
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def bought_courses(self):
        return list(Order.objects.filter(student_id=self.id).values_list("course__name", flat=True))

    def interested_in_topics(self):
        return list(self.interested_in.values_list("name", flat=True))


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        (0, 'Cancelled'),
        (1, 'Order Confirmed')
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    levels = models.PositiveIntegerField(default=5)
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    order_date = models.DateField(default=timezone.now)

    def __str__(self):
        return 'course=' + self.course.name + ' Student=' + self.student.username


class Interest(models.Model):
    interested = models.CharField(max_length=200)
    levels = models.IntegerField(default=1)
    comments = models.CharField(max_length=200, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=20, default="", null=True)
    orders = models.ManyToManyField(Order)
    student = models.ForeignKey(
        Student, on_delete=models.DO_NOTHING, null=True)
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE, null=True)
