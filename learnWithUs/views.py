from django.shortcuts import render, get_object_or_404, redirect
from .decorators import unauthenticated_user, role_required, staff_only
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Role, Course, Teacher, Student, CustomUser, Department,SidebarItem
from .forms import SignUpForm,SidebarItemForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import Permission, Group
# from django.http import HttpResponseForbidden
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import user_passes_test
# Create your views here.

# @has_permission('Can view dashboard')






def test_condition(request):
    username = request.GET.get('username')
    email = request.GET.get('email')
    error_message = ""
    if username:
        user = CustomUser.objects.filter(username__iexact=username).first()
        if user:
            error_message += "username <{}> ".format(username)
    if email:
        user = CustomUser.objects.filter(email__iexact=email).first()
        if user:
            error_message += "email <{}> ".format(email)
    error_message += "already exist"
    if not error_message:
        error_message = "No errors."
    return JsonResponse({"error_message": error_message})







@method_decorator(login_required, name='dispatch')
@method_decorator(role_required('admin'), name='dispatch')
class RoleListView(ListView):
    model = Role
    template_name = 'role_list.html'
    context_object_name = 'roles'


@method_decorator(login_required, name='dispatch')
@method_decorator(role_required('admin'), name='dispatch')
class RoleCreateView(CreateView):
    model = Role
    template_name = 'role_create.html'
    fields = ['name']
    success_url = reverse_lazy('role_list')


@method_decorator(login_required, name='dispatch')
@method_decorator(role_required('admin'), name='dispatch')
class RoleUpdateView(UpdateView):
    model = Role
    template_name = 'role_create.html'
    fields = ['name']
    success_url = reverse_lazy('role_list')


@method_decorator(login_required, name='dispatch')
@method_decorator(role_required('admin'), name='dispatch')
class RoleDeleteView(DeleteView):
    model = Role
    template_name = 'role_confirm_delete.html'
    success_url = reverse_lazy('role_list')

# @method_decorator(login_required, name='dispatch')
# @method_decorator(role_required('admin'), name='dispatch')
# class PermissionListView(ListView):
#     model = Permission
#     template_name = 'permission_list.html'
#     context_object_name = 'permissions'

# @method_decorator(login_required, name='dispatch')
# @method_decorator(role_required('admin'), name='dispatch')
# class PermissionCreateView(CreateView):
#     model = Permission
#     template_name = 'permission_create.html'
#     fields = ['name']
#     success_url = reverse_lazy('permission_list')

# @method_decorator(login_required, name='dispatch')
# @method_decorator(role_required('admin'), name='dispatch')
# class PermissionUpdateView(UpdateView):
#     model = Permission
#     template_name = 'permission_update.html'
#     fields = ['name']
#     success_url = reverse_lazy('permission_list')

# @method_decorator(login_required, name='dispatch')
# @method_decorator(role_required('admin'), name='dispatch')
# class PermissionDeleteView(DeleteView):
#     model = Permission
#     template_name = 'permission_delete.html'
#     success_url = reverse_lazy('permission_list')


@login_required
def assign_role(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if not request.user.is_superuser:
        return redirect('dashboard')
    if request.method == 'POST':
        # get the selected role id from the form
        role_id = request.POST.get('role')

        # get the selected permissions from the form
        # permission_ids = request.POST.getlist('permissions')
        # permissions = Permission.objects.filter(id__in=permission_ids)

        # assign the role to the user
        role = Role.objects.get(id=role_id)
        user.role = role
        user.save()

        # assign the permissions to the role
        # for permission in permissions:
        #     role_permission = RolePermission.objects.get_or_create(role=role, permission=permission)
        # role_permission.save()
        # role.permissions.set(permissions)
        role.save()

        return redirect('assign_role', user_id=user_id)

    roles = Role.objects.all()
    # permissions = Permission.objects.all()
    context = {
        'user': user,
        'roles': roles,
        # 'permissions': permissions,
    }
    return render(request, 'assign_role.html', context)

# @user_passes_test(lambda user: not request.user.is_authenticated, redirect_to='home')
@unauthenticated_user
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            if user.is_superuser:
                request.session['your_self'] = 'Superuser'
                return redirect('dashboard')
            elif Student.objects.filter(user=user).exists():
                request.session['your_self'] = 'Student'
                return redirect('course_list')
            elif Teacher.objects.filter(user=user).exists():
                request.session['your_self'] = 'Teacher'
                return redirect('teacher_list')
            else:
                return redirect('course_list')
        else:
            messages.error(
                request, "Invalid username or password. Please try again.")
    return render(request, "authenticate/login.html")


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged Out..."))
    return redirect('course_list')


@unauthenticated_user
def signup(request):
    courses = Course.objects.all()
    # roles = Role.objects.all()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            confirm_password = form.cleaned_data.get('password2')
            name = request.POST.get('name')
            description = request.POST.get('description')
            image = request.POST.get('image')
            # role_id = request.POST.get('role')
            define_yourself = request.POST.get('define_your_self')

            if password != confirm_password:
                error_message = "Passwords do not match"
                return render(request, 'signup.html', {'form': form, 'error_message': error_message})
            user = CustomUser(username=username, email=email,
                              first_name=first_name, last_name=last_name,password = confirm_password)
            user.save()
            if define_yourself == 'student':
                course_id = request.POST.get('defineYourCourse')
                courses = request.POST.getlist('courses')
                student = Student(user_id=user.id)
                if courses:
                    for course_id in courses:
                        try:
                            course = Course.objects.get(id=course_id)
                        except Course.DoesNotExist:
                            continue
                    student.courses.add(course)
                    # student.courses.set(courses)
                else:
                    error_message = "Need To Select a Course"
                    return render(request, 'signup.html', {'form': form, 'error_message': error_message })
                student.save()
                subject = 'New Course Assignment'
                message = f'You have been signup to our website. Your username is {username} and your password in {password}'
                from_email = 'noreply@example.com'
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list)
                login(request, user)
                authenticate(request, user=user)
                return redirect('course_list')
            elif define_yourself == 'teacher':
                specialty = request.POST.get('tellUsYourSpeciality')
                teacher = Teacher(user_id=user.id, specialty=specialty)
                teacher.save()
                if all([name,description,image]):
                    Course.objects.create(
                        name=name,
                        description=description,
                        image=image,
                        )
                    teacher.courses.add(course)
                subject = 'You are signup into the Online Learning Platform as Teacher'
                message = f'You have been signup to our website. Your username is {username} and your password in {password}'
                from_email = 'noreply@example.com'
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list)
                authenticate(request, user=user)
                login(request, user)
                return redirect('teacher_list')
            else:
                error_message = "Must have to say who are you?"
                return render(request, 'signup.html', {'form': form, 'error_message': error_message})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'courses': courses, })


def get_user_details(request,pk):
    search_user = CustomUser.objects.filter(pk=pk)
    return render(request,'user_details.html',{'search_user':search_user})

@login_required
@role_required('admin')
def user_update(request,pk):
    user = get_object_or_404(CustomUser,pk=pk)
    lastURL = request.session.get('lastURL')
    if request.method == 'POST':
        department_id = request.POST.get('department')
        form = SignUpForm(request.POST, instance=user)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            user.first_name = first_name if first_name else user.first_name
            user.last_name = last_name if last_name else user.last_name
            user.email = email if email else user.email
            user.username = username if username else user.username
            department_id = request.POST.get('department')
            user.save()
            if department_id:
                student_exists = Student.objects.filter(user=user).exists()
                teacher_exists = Teacher.objects.filter(user = user).exists()
                if student_exists:
                    department = Department.objects.get(pk=department_id)
                    student = get_object_or_404(Student,user=user)
                    student.department = department
                    student.save()
                elif teacher_exists:
                    department = Department.objects.get(pk=department_id)
                    teacher = get_object_or_404(Teacher,user = user)
                    teacher.department = department
                    teacher.save()
            lastURL = request.session.pop('lastURL', None)
            print(lastURL)
        return redirect(lastURL or 'course_list')
    else:
        teachers = Teacher.objects.all()
        students = Student.objects.all()
        departments = Department.objects.all()
        request.session['lastURL'] = request.META.get('HTTP_REFERER')
        context = {'teachers': teachers, 
                   'pk': user.id, 'students': students,'user':user,'departments':departments}
        return render(request, 'update_user.html', context)


@login_required
@role_required('admin')
def user_delete(request,pk):
    user = get_object_or_404(CustomUser,pk=pk)
    user.delete()
    lastURL= request.META.get('HTTP_REFERER')
    return redirect(lastURL)
    
@login_required
@role_required('admin')
def create_teacher(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('email')
        password = "password"
        user = CustomUser.objects.create_user(
        username=username, email=email, first_name=first_name, last_name=last_name,password=password)
        specialty = request.POST.get('tellUsYourSpeciality')
        teacher = Teacher(user_id=user.id, specialty=specialty)
        department_id = request.POST.get('department')
        if department_id:
                department = Department.objects.get(pk=department_id)
                teacher.department = department
        teacher.save()
        subject = 'Welcome to our Website as a Teacher'
        message = f'You have been signup by admin to our website. Your username is {username} and your password in {password}'
        from_email = 'noreply@example.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        return redirect('teacher_list')
    else:
        courses = Course.objects.all()
        departments = Department.objects.all() 
        form = SignUpForm()
    return render(request, 'create_teacher.html', {'form': form, 'courses': courses,'departments':departments})


def search_teachers(request):
    query = request.GET.get('q')
    results = []
    if query:
        teachers = Teacher.objects.filter(user__email__icontains=query)
        for teacher in teachers:
            results.append({'id': teacher.id, 'email': teacher.user.email, 'username': teacher.user.username})
    return JsonResponse({'results': results})




def search_students(request):
    query = request.GET.get('q')
    results = []
    if query:
        students = Student.objects.filter(user__email__icontains=query)
        for student in students:
            results.append({'id': student.id, 'email': student.user.email,'username': student.user.username})
    return JsonResponse({'results': results})

def ajax_test(request):
    if request.method == 'GET':
        data = {'response': f'The message you sent was:'}
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'This view only accepts POST requests.'})

def all_users(request):
    users = CustomUser.objects.all()
    results = []
    for user in users:
        user_type = ''
        if user.role:
            user_type = user.role.name
        elif Teacher.objects.filter(user=user).exists():
            user_type = 'T'
        elif Student.objects.filter(user=user).exists():
            user_type = 'S'
        results.append({'id': user.id, 'email': user.email, 'username': user.username,'user_type':user_type,'user_id':user.id})
    return JsonResponse({'results': results})


def search_users(request):
    query = request.GET.get('q')
    results = []
    if query:
        users = CustomUser.objects.filter(Q(email__icontains=query) | Q(username__icontains=query))
    else:
        users = CustomUser.objects.all()
    for user in users:
        user_type = ''
        if user.role:
            user_type = user.role.name
        elif Teacher.objects.filter(user=user).exists():
            user_type = 'T'
        elif Student.objects.filter(user=user).exists():
            user_type = 'S'
        results.append({'id': user.id, 'email': user.email, 'username': user.username,'user_type':user_type,'user_id':user.id})
    return JsonResponse({'results': results})


@login_required
@role_required('admin')
def create_student(request):
    course = Course.objects.all()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = "password"
            user = CustomUser.objects.create_user(
                username=username, email=email, first_name=first_name, last_name=last_name)
            student = Student(user_id=user.id)
            courses = request.POST.getlist('courses')
            department_id = request.POST.get('department')
            if department_id:
                department = Department.objects.get(pk=department_id)
                student.department = department
            student.save()
            if courses:
                    student.courses.set(courses)
            subject = 'Welcome to our website as a Student'
            message = f'You have been signup by admin to our website. Your username is {username} and your password in {password}'
            from_email = 'noreply@example.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)    
            return redirect('student_list')
    else:
        form = SignUpForm()
        departments = Department.objects.all()
    return render(request, 'create_student.html', {'form': form, 'course': course,'departments':departments})


@login_required
@role_required('admin')
def course_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        teacher_id = request.POST.get('teacher')
        image = request.POST.get('image')
        department_id = request.POST.get('department')
        if department_id:
            department = Department.objects.get(id= department_id)
        else:
            error_message = "Must have to provide the name of department"
            return render(request,"course_form.html",context={'error_message':error_message})
        course = Course.objects.create(
            name=name,
            description=description,
            image=image,
            department = department
        )
        if teacher_id:
            teacher = Teacher.objects.get(id=teacher_id)
            teacher.courses.add(course.id)
        students = request.POST.getlist('students')
        if students:
            for student_id in students:
                student = Student.objects.get(id=student_id)
                student.courses.add(course.id)
        return redirect('course_list')
    else:
        teachers = Teacher.objects.all()
        students = Student.objects.all()
        departments = Department.objects.all()
        context = {'teachers': teachers, 'students': students,"departments":departments}
        return render(request, 'course_form.html', context)


@login_required
@role_required('admin')
def course_update(request, pk):
    course = Course.objects.get(pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        teacher_id = request.POST.get('teacher')
        image = request.POST.get('image')
        department_id = request.POST.get('department')
        course.name = name if name else course.name
        course.description = description if description else course.description
        course.image = image if image else course.image
        department_id = request.POST.get('department')
        if department_id:
            department = Department.objects.get(id= department_id)
            course.department = department
        course.save()
        course.teachers.clear()
        if teacher_id:
            teacher = Teacher.objects.get(id=teacher_id)
            if not teacher.courses.filter(id=course.id).exists():
                teacher.courses.add(course)
        students = request.POST.getlist('students')
        course.students.clear()
        if students:
            for student_id in students:
                student = Student.objects.get(id=student_id)
                if not student.courses.filter(id=course.id).exists():
                    student.courses.add(course)
        return redirect('course_list')
    else:
        teachers = Teacher.objects.all()
        students = Student.objects.all()
        departments = Department.objects.all()
        context = {'teachers': teachers, 'course': course,
                   'pk': pk,"departments":departments,'students': students}
        return render(request, 'course_update.html', context)

class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'
    # paginate_by = 10

@method_decorator(login_required, name='dispatch')
@method_decorator(role_required('admin'), name='dispatch')
class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'course_confirm_delete.html'
    success_url = reverse_lazy('course_list')


def teacher_list_view(request):
    teachers = Teacher.objects.prefetch_related('courses')
    context = {'teachers': teachers}
    return render(request, 'teacher_list.html', context)


def student_list_view(request):
    students = Student.objects.prefetch_related('courses')
    context = {'students': students}
    return render(request, 'student_list.html', context)


def department_list_view(request):
    departments = Department.objects.all()
    return render(request,"all_departments.html",context={'departments':departments})


def create_department(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Department.objects.create(name=name)
        else:
            error_message = "Must have to provide the name of department"
            return render(request,"create_department.html",context={'error_message':error_message})
        return redirect("department_list")
    else:
        return render(request,"create_department.html")
def update_department(request,pk):
    department = Department.objects.get(pk=pk)
    if request.method == "POST":
        name = request.POST.get("name")
        department.name = name if name else department.name
        department.save()
        return redirect("department_list")
    else:
        return render(request,"update_department.html",context={'department':department,"pk":pk})
def delete_department(request,pk):
    department =  get_object_or_404(Department,pk=pk)
    department.delete()
    return redirect("department_list")

@login_required
@role_required('admin')
def dashboard(request):
    teacher = Teacher.objects.count()
    student = Student.objects.count()
    course = Course.objects.count()
    return render(request, 'dashboard.html', context={'teacher': teacher, 'student': student, 'course': course})


def sidebar_all(request):
    sidebar_items = SidebarItem.objects.all().order_by('position')
    return render(request, 'sidebar/index.html', {'sidebar_items': sidebar_items})



def sidebar_create(request):
    if request.method == 'POST':
        form = SidebarItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.parent = None  # set parent to None for top-level items
            form.position = SidebarItem.objects.count() + 1
            item.save()
            return redirect('sidebar_list')  # redirect to prevent resubmission
    else:
        form = SidebarItemForm()
    sidebar_items = SidebarItem.objects.all()
    return render(request, 'create.html', {'form': form, 'sidebar_items': sidebar_items})


def sidebar_update(request, pk):
    sidebar_item = get_object_or_404(SidebarItem, pk=pk)
    if request.method == 'POST':
        form = SidebarItemForm(request.POST, instance=sidebar_item)
        if form.is_valid():
            form.save()
            return redirect('sidebar_list')
    else:
        form = SidebarItemForm(instance=sidebar_item)
    return render(request, 'sidebar/form.html', {'form': form})



def delete(request, pk):
    sidebar_item = get_object_or_404(SidebarItem, pk=pk)
    if request.method == 'POST':
        sidebar_item.delete()
        return redirect('sidebar:index')
    return render(request, 'sidebar/delete.html', {'sidebar_item': sidebar_item})





def group_permissions(request):
    groups = Group.objects.all()
    context = {
        'groups': groups
    }
    return render(request, 'group_permissions.html', context)