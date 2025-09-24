from django import forms
from register.models import students_table
from register.models import marks_table
from register.models import teachers_table

class students_tableform(forms.ModelForm):
    class Meta:
        model = students_table
        fields = ['rollno', 'name', 'grade', 'section', 'pwd']

class marks_tableform(forms.ModelForm):
    class Meta:
        model = marks_table
        fields = ['english', 'hindi', 'social_science', 'science', 'mathematics', 'student']

class teachers_tableform(forms.ModelForm):
    class Meta:
        model = teachers_table
        fields = ['name', 'pwd', 'subject', 'doj']
