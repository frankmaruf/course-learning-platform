from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Course, Student, Teacher
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

# @receiver(post_save, sender=Course)
# def notify_teacher(sender, instance, **kwargs):
#     if instance.notified:
#         return
#     subject = 'New Course Assignment'
#     message = f'You have been assigned to teach {instance.name}.'
#     from_email = 'noreply@example.com'
#     recipient_list = [instance.teacher.email]
#     send_mail(subject, message, from_email, recipient_list)
#     instance.notified = True
#     instance.save()
    
# @receiver(post_save, sender=Student)
# def notify_student(sender, instance, **kwargs):
#     subject = 'New Course Signup'
#     message = f'You have signed up for learn {instance.course.name}.'
#     from_email = 'noreply@example.com'
#     recipient_list = [instance.user.email]
#     send_mail(subject, message, from_email, recipient_list)
    
# @receiver(post_save, sender=Teacher)
# def notify_teacher_after_signup(sender, instance, **kwargs):
#     password = 'password' # set your desired plain text password here
#     instance.user.set_unusable_password()
#     instance.user.set_password(password)
#     instance.user.save()
#     subject = 'You are signup into the Online Learning Platform'
#     course = instance.course if hasattr(instance, 'course') else None
#     course_name = course.name if course else ''
#     message = f'You have signed up for Teach {course_name}. your password is {password}, your username is {instance.user.username}'
#     from_email = 'noreply@example.com'
#     recipient_list = [instance.user.email]
#     send_mail(subject, message, from_email, recipient_list)

# Start
# @receiver(post_save, sender=Teacher)
# def notify_teacher_after_signup(sender, instance, created, **kwargs):
#     password = 'password'
#     if instance.user.password:
#         message = f'Your username is {instance.user.username}. your password is {password}'
#     else:
#         instance.user.set_unusable_password()
#         instance.user.set_password(password)
#         instance.user.save()
#         message = f'Your username is {instance.user.username}. Your password is {password}'
#     subject = 'You are signup into the Online Learning Platform as Teacher'
    # Mid
    # course = instance.course if hasattr(instance, 'course') else None
    # course_name = course.name if course else ''
    # Mid
    # from_email = 'noreply@example.com'
    # recipient_list = [instance.user.email]
    # send_mail(subject, message, from_email, recipient_list)
    # End
# Start
# @receiver(post_save, sender=Student)
# def notify_student_after_signup(sender, instance, **kwargs):
#     password = 'password'
#     instance.user.set_unusable_password()
#     instance.user.set_password(password)
#     instance.user.save()
#     student = Student.objects.get(id=instance.id)'
# Mid
    # course_list = []
    # course_str_name = ""
    # for course in student.courses.all():
    #     course_list.append(course.name)
    #     print(course.name)
    # if course_list:
    #     course_str_name = ", ".join(course_list)
    #     message = f"Welcome {instance.user.username}! You are now enrolled in the following courses: {course_str_name}. Here is your password <{password}>"
    #     # send notification to student with message
    # else:
    #     message = f"Welcome {instance.user.username}! You have not been enrolled in any courses yet. here is your password <{password}>"
        # send notification to student with message
    # print(instance.id)
    # Mid
    # subject = 'You Have signup as Student'
    # message = f'Your username is {instance.user.username} and Your password is {password}, '
    # from_email = 'noreply@example.com'
    # recipient_list = [instance.user.email]
    # send_mail(subject, message, from_email, recipient_list)
    
# End