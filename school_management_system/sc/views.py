from django.shortcuts import render, redirect, get_object_or_404
from .forms import students_tableform
from .forms import marks_tableform
from .forms import teachers_tableform
from register.models import students_table
from register.models import marks_table
from register.models import teachers_table
from django.contrib import messages

import mysql.connector as mcon

dic={}

#To enter student details
def std_details(request):
    if request.method == 'POST':
        searchrollno=request.POST.get('rollno')
        searchname=request.POST.get('name')
        searchngrade=request.POST.get('grade')
        data=request.POST
        form = students_tableform(request.POST or None)
        if form.is_valid():
            form.save()
            import mysql.connector
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              password=<password>,
              database="school_management"
            )

            mycursor = mydb.cursor()
            stuid = students_table.objects.filter(rollno=searchrollno, name=searchname, grade=searchngrade).first()
            if stuid:
                stuid = stuid.student_id
            stuid=(stuid,)
            sql = "INSERT INTO register_marks_table (english, hindi, social_science, science, mathematics, student_id) VALUES (0, 0, 0, 0, 0, %s)"
            mycursor.execute(sql, stuid)
            mydb.commit()
            messages.success(request, ('You are now officially a student'))
        return render(request, 'enter_std_details.html')

    else:
        return render(request, 'enter_std_details.html', {})
    
#To enter teacher details
def tch_details(request):
    if request.method == 'POST':
        form = teachers_tableform(request.POST or None)
        if form.is_valid():
            form.save()
        messages.success(request, ('You are now officially a teacher'))
        return render(request, 'enter_tch_details.html')
    else:
        return render(request, 'enter_tch_details.html', {})

def details(request):
    students = students_table.objects.all()
    return render(request, 'view_student_details.html', {'all': students})

#To get the ID of student for whom you want to enter marks
def dropdownsearch(request):
    if request.method=="POST":
        searchrollno=request.POST.get('rollno')
        searchname=request.POST.get('name')
        searchngrade=request.POST.get('grade')
        stusearch=students_table.objects.filter(rollno=searchrollno, name=searchname, grade=searchngrade)
        return render(request,'select_student.html',{"data":stusearch})
    else:
        displaystu=students_table.objects.all()
        return render(request,'select_student.html',{"data":displaystu})

#To login as teacher or student
def login(request):
    global subject
    global sid
    if request.method=="POST":
        val=request.POST.get('val')
        data=request.POST
        val=data['val']
        pwd = data['pwd']
        id_status_list = students_table.objects.values_list('pwd')
        id_status_lis = teachers_table.objects.values_list('pwd')
        subject = teachers_table.objects.filter(teacher_id=val).first()
        sid = students_table.objects.filter(student_id=val).first()
        if sid:
            sid = sid.student_id
        if subject:
            subject = subject.subject
            print(subject)           
        if '2038' in str(val) and str(pwd) in str(id_status_lis) and str(pwd) != '':
            messages.success(request, str('Welcome Teacher'))
            return render(request, 'teacher.html', {})
        elif '19204' in str(val) and str(pwd) in str(id_status_list) and str(pwd) != '':
            messages.success(request, ('Welcome Student'))
            return render(request, 'student.html', {})
        else:
            messages.success(request, ('User Credentials Invalid'))
        
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')



#To enter marks of student in each subject
def enter_marks(request):
    if request.method == 'POST':
        # Retrieve data from POST request
        updt_student_id = request.POST.get('student')
        updt_subject = subject.lower()
        marks = request.POST.get('marks')

        # Validate input
        if not updt_student_id or not updt_subject or not marks:
            messages.error(request, 'All fields are required.')
            return render(request, 'enter_marks.html')

        # Define subject field mapping
        subject_dict = {
            'english': 'english',
            'hindi': 'hindi',
            'social_science': 'social_science',
            'science': 'science',
            'mathematics': 'mathematics'
        }

        # Check if the subject is valid
        if updt_subject not in subject_dict:
            messages.error(request, 'Invalid subject')
            return render(request, 'enter_marks.html')

        try:
            connection = mcon.connect(user='root', host='localhost', password=<password>, database='school_management')
            if connection.is_connected():
                cursor = connection.cursor()

                # Update the mark for the specified subject
                column_name = subject_dict[updt_subject]
                update_query = f'UPDATE register_marks_table SET {column_name} = %s WHERE student_id = %s'
                cursor.execute(update_query, (marks, updt_student_id))
                connection.commit()

                messages.success(request, f'Marks entered successfully for {updt_subject}.')
                
                # Close the cursor and connection
                cursor.close()
                connection.close()
            else:
                messages.error(request, 'Failed to connect to the database.')

        except mcon.Error as err:
            messages.error(request, f"Error: {err}")

        return render(request, 'enter_marks.html')

    else:
        return render(request, 'enter_marks.html')



#To view marks entered (as teacher)
def view_marks(request):
    if request.method=="POST":
        searchstudent=request.POST.get('student')
        markssearch=marks_table.objects.filter(student=searchstudent)
        return render(request,'view_marks.html',{"data":markssearch})
    else:
        displaymarks=marks_table.objects.all()
        return render(request,'view_marks.html',{"data":displaymarks})

#To view marks entered (as student)
def view_marks_as_std(request):
    displaymarks=marks_table.objects.filter(student_id=sid)
    return render(request,'view_marks_as_std.html',{"data":displaymarks})

# To update marks
import mysql.connector as mcon

def update_marks(request):
    if request.method == 'POST':
        # Retrieve data from POST request
        updt_student_id = request.POST.get('student_id')
        updt_subject = request.POST.get('subject')
        new_marks = request.POST.get('new_marks')

        # Validate input
        if not updt_student_id or not updt_subject or not new_marks:
            messages.error(request, 'All fields are required.')
            return render(request, 'update_marks.html')

        # Define subject field mapping
        subject_dict = {
            'english': 'english',
            'hindi': 'hindi',
            'social_science': 'social_science',
            'science': 'science',
            'mathematics': 'mathematics'
        }

        # Check if the subject is valid
        if updt_subject not in subject_dict:
            messages.error(request, 'Invalid subject')
            return render(request, 'update_marks.html')

        try:
            connection = mcon.connect(user='root', host='localhost', password=<password>, database='school_management')
            if connection.is_connected():
                cursor = connection.cursor()

                # Update the mark for the specified subject
                column_name = subject_dict[updt_subject]
                update_query = f'UPDATE register_marks_table SET {column_name} = %s WHERE student_id = %s'
                cursor.execute(update_query, (new_marks, updt_student_id))
                connection.commit()

                messages.success(request, f'Marks updated successfully for {updt_subject}.')
                
                # Close the cursor and connection
                cursor.close()
                connection.close()
            else:
                messages.error(request, 'Failed to connect to the database.')

        except mcon.Error as err:
            messages.error(request, f"Error: {err}")

        return render(request, 'enter_marks.html')

    else:
        return render(request, 'enter_marks.html')

def view_tch_details(request):
    teachers = teachers_table.objects.all()
    return render(request, 'view_tch_details.html', {'all': teachers})

def home(request):
    return render(request, 'home.html')

def teacher(request):
    return render(request, 'teacher.html')

def student(request):
    return render(request, 'student.html')
