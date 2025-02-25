from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.dateformat import DateFormat
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Student, Teacher, Parent


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'fullname')
    readonly_fields = ('fullname', 'email')
    fields = ('user', 'fullname', 'email', 'birthday', 'coding_experience', 'parent')

    def fullname(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def email(self, obj):
        return obj.user.email

    fullname.short_description = 'Fullname'
    email.short_description = 'Email'


class ParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'fullname', 'get_children')
    readonly_fields = ('fullname', 'email', 'get_children_email', 'get_children')
    fields = ('user', 'fullname', 'email', 'get_children_email', 'get_children')

    def fullname(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def email(self, obj):
        return obj.user.email

    def get_children_email(self, obj):
        return ", ".join([str(child.user.email) for child in obj.get_children()])

    def get_children(self, obj):
        return ", ".join([str(child.user.username) for child in obj.get_children()])

    fullname.short_description = 'Fullname'
    email.short_description = 'Email'
    get_children_email.short_description = 'Children Email'
    get_children.short_description = 'Children'


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'fullname')
    readonly_fields = ('fullname', 'email')
    fields = ('user', 'fullname', 'email', 'course')

    def fullname(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def email(self, obj):
        return obj.user.email

    fullname.short_description = 'Fullname'
    email.short_description = 'Email'


class CustomUserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'full_name', 'user_type', 'date_joined')
    ordering = ('-date_joined',)

    def user_type(self, obj):
        if Student.objects.filter(user=obj).exists():
            return 'Student'
        elif Parent.objects.filter(user=obj).exists():
            return 'Parent'
        elif Teacher.objects.filter(user=obj).exists():
            return 'Teacher'
        elif obj.is_staff:
            return 'Admin'
        else:
            return 'Unknown'

    user_type.short_description = 'User Type'

    def full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name

    full_name.short_description = 'Full Name'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Student, StudentAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Teacher, TeacherAdmin)
