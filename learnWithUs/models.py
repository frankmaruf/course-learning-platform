from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class SidebarItem(models.Model):
    title = models.CharField(max_length=50)
    url = models.URLField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    position = models.PositiveIntegerField()

    class Meta:
        ordering = ['position']
    def __str__(self):
        return self.title



class Role(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.name

class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users')
    REQUIRED_FIELDS = ['role']


class Department(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name





class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL, related_name='courses')
    image = models.ImageField(upload_to='course_images/',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.name




class Student(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, through='CourseStudentNotification', related_name='students')
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CourseStudentNotification(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    notified = models.BooleanField(default=False)

class Teacher(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course,through="CourseTeacherNotification",related_name="teachers")
    specialty = models.CharField(max_length=255)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL, related_name='teachers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CourseTeacherNotification(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    notified = models.BooleanField(default=False)