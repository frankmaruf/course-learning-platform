from django.contrib import admin
from .models import Role,Course,Student,Teacher,CustomUser, Department
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'role']
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('role',)}),)
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Department)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    ordering = ['name']



@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    ordering = ['name']
    
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'user_first_name','courses_list')
    search_fields = ['user__email']
    ordering = ['id']
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'First Name'
    def courses_list(self, obj):
        return ', '.join([course.name for course in obj.courses.all()])
    courses_list.short_description = 'Courses'

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'user_first_name','courses_list')
    search_fields = ['user__email']
    ordering = ['id']
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'First Name'
    def courses_list(self, obj):
        return ', '.join([course.name for course in obj.courses.all()])
    courses_list.short_description = 'Courses'