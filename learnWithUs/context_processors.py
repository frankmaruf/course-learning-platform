from .models import Student, Teacher,SidebarItem

def user_role(request):
    user = request.user
    if user.is_authenticated:
        if user.role:
            return {'user_role': user.role.name}
        elif Student.objects.filter(user=user).exists():
            return {'user_role': 'Student'}
        elif Teacher.objects.filter(user=user).exists():
            return {'user_role': 'Teacher'}
    return {}


def sidebar(request):
    sidebar_items = SidebarItem.objects.all()
    return {'sidebar_items': sidebar_items}