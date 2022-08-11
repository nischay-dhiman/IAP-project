import decimal

from django.contrib import admin
from django.contrib import admin
from django.db import models
from django.db.models import F

from .models import Topic, Course, Student, Order


class CourseInline(admin.TabularInline):
    model = Course


class TopicAdmin(admin.ModelAdmin):
    inlines = [CourseInline]


class CourseAdmin(admin.ModelAdmin):
    actions = ['apply_discount']

    def apply_discount(self, request, queryset):
        queryset.update(price=F('price') * decimal.Decimal('0.9'))

    apply_discount.short_description = 'Apply 10% discount'

class StudentAdmin(admin.ModelAdmin):
    model = Student
    list_display = ("first_name", "last_name", "registered_courses")



# Register your models here.
admin.site.register(Topic, TopicAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)


# admin.site.register(Topic)
# admin.site.register(Course)
# admin.site.register(Student)
admin.site.register(Order)
