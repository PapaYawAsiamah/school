from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from .models import Student

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404



@login_required(login_url="/dashboard/")
def Dashboard(request):
    total_students = Student.objects.count()
    context = {
        'total_students': total_students,
        # Add other context variables as needed
    }
    return render(request, 'pages/dashboard.html', context)



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username = username).exists():
            user = authenticate(username=username, password=password)
        
            if user is not None:
            # Correctly pass the 'user' object to login function
                login(request, user)
                return redirect('/dashboard')  # Redirect to the dashboard after login
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.info(request,'user does not exist')
            return redirect('/')
    
    return render(request, 'pages/login.html')

# Check if the user is an admin
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        password_confirm = request.POST['password2']
        
        if password == password_confirm:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('/')
            except Exception as e:
                messages.error(request, 'Username already exists.')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'pages/register.html')



def student_list(request):
    print("hello")
    students = Student.objects.all()
    
    return render(request, 'pages/students/student.html', {'students': students})


def add_student(request):
    if request.method == "POST":
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        other_names = request.POST.get('otherNames', '')
        dob = request.POST['dob']
        residence = request.POST['residence']
        parent_info = request.POST['parentInfo']
        grade = request.POST['grade']
        
        # Combine first, last, and other names into full name
        full_name = f"{first_name} {other_names} {last_name}".strip()
        
        # Save student to the database
        student = Student.objects.create(
            full_name=full_name,
            dob=dob,
            residence=residence,
            parent_info=parent_info,
            grade=grade
        )
        
        return JsonResponse({'message': 'Student added successfully!'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def edit_student(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, id=student_id)
        student.name = request.POST.get('name')
        student.age = request.POST.get('age')
        student.grade = request.POST.get('grade')
        student.save()
        return JsonResponse({'message': 'Student updated successfully!'})

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return JsonResponse({'message': 'Student deleted successfully!'})


def student_search(request):
    if 'query' in request.GET:
        query = request.GET['query']
        students = Student.objects.filter(
            first_name__icontains=query
        ) | Student.objects.filter(
            last_name__icontains=query
        ) | Student.objects.filter(
            other_names__icontains=query
        )
        results = [{'id': student.id, 'full_name': f"{student.first_name} {student.last_name} {student.other_names}"} for student in students]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)