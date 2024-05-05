from django.shortcuts import redirect, render
from humanresource.models import Hr

from empmanage.models import Employee,Notifications,EmployeeSalary,LeaveRequest,RemainLeave
from hashlib import sha256
# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            
            user =  Hr.objects.filter(email=username,password=sha256(password.encode('utf-8')).hexdigest())
            if len(user)==1:
                print('login true')
                user = Hr.objects.get(email=username)
                response = redirect('/hr/dashboard/')
                response.set_cookie('email', username)
                response.set_cookie('username',user.name)
                return response
            else:
                return render(request,'hr_login_page.html',{'error':'Invalid email or password'})
        except Exception as e:
            return render(request,'hr_login_page.html',{'error':'Internal Server Error'})
    return render(request,'hr_login_page.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        try:
            emp = Hr.objects.filter(email=email)
            if len(emp)==0:
                hr = Hr(
                name=name,email=email,password=sha256(password.encode('utf-8')).hexdigest(),
                phone_number=phone_number)
                hr.save()
                employee = Employee(
                name=name,email=email,password=sha256(password.encode('utf-8')).hexdigest(),
                phone_number=phone_number)
                employee.save()
                return redirect('/hr/login')
            else:
                return render(request,'hr_register_page.html',{'error':'User Already Exists'})
            
        except Exception as e:
            print(e)
    return render(request,'hr_register_page.html')

def dashboard(request):
    name = request.COOKIES.get('username') 
    emp = Employee.objects.all()
    if request.method =='POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        if title:
            try:
                emp = Employee.objects.all()
                noti = Notifications(title=title,message=message)
                noti.save()
                return render(request,'hr_dashboard.html',{'name':name,'employees':emp})
            except Exception as e:
                print(e)
    
    return render(request,'hr_dashboard.html',{'name':name,'employees':emp})

def view_employee(request):

    emp = Employee.objects.all()
    return render(request,'hr_dashboard_viewemp.html',{'employees':emp})

def edit_emp_profile(request):
    id = request.GET.get('id')
    emp = Employee.objects.get(id=id)
   
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        department = request.POST.get('department')
        position = request.POST.get('position')
        hired_date = request.POST.get('hired_date')

        try:
            emp.name=name
            emp.email=email
            emp.phone_number=phone_number
            emp.address=address
            emp.department=department
            emp.position=position
            emp.hired_date=hired_date
            emp.save()
            return redirect('/hr/dashboard/view')
        except Exception as e:
            print(e)
    return render(request,'emp_edit_profile.html',{'emp':emp})

def delete_emp(request):
    id = request.GET.get('id')
    emp = Employee.objects.get(id=id)
    emp.delete()
    return redirect('/hr/dashboard/')

def logout(request):
    response = redirect('/hr/login/')
    response.delete_cookie('email')
    response.delete_cookie('username')
    return response

def salary(request):
    if request.method=='POST':
        emp_id = request.POST.get('employee')
        salary = request.POST.get('salary')
        print(emp_id,salary)
        try:
            emp = Employee.objects.get(id=emp_id)
            emp_salary = EmployeeSalary(email=emp.email,salary=salary)
            emp_salary.save()
            return redirect('/hr/dashboard/')
        except Exception as e:
            print(e)
    try:
        emp = Employee.objects.all()
        return render(request,'emp_salary_edit.html',{'employees':emp})
    except Exception as e:
        print(e)

def viewprofile(request):
    id = request.GET.get('id')
    emp = Employee.objects.get(id=id)
    return render(request,'emp_view_profile.html',{'employee':emp})

def leave_request_status(request):
    emp_leave=LeaveRequest.objects.filter(leave_status__isnull=True)
    return render(request,'emp_leave_request.html',{'leaves':emp_leave})
    

def accept_leave(request):
    id = request.GET.get('id')
    
    leave= LeaveRequest.objects.get(id=id)
    difference = (leave.leave_date_to - leave.leave_date_from).days
    leave.leave_status='Accepted'
    leave.save()
    leave_count= RemainLeave(email=leave.email,total_leave=difference)                  
    leave_count.save()
    return redirect('/hr/dashboard/leave/')

def reject_leave(request):
    id = request.GET.get('id')
   
    leave= LeaveRequest.objects.get(id=id)
    leave.leave_status='Rejected'
    leave.save()
    return redirect('/hr/dashboard/leave/')