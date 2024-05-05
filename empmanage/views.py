from django.shortcuts import redirect, render
from empmanage.models import Employee,Notifications,EmployeeSalary,LeaveRequest,RemainLeave
from hashlib import sha256

def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            
            user =  Employee.objects.filter(email=username,password=sha256(password.encode('utf-8')).hexdigest())
            if len(user)==1:
                print('login true')
                user = Employee.objects.get(email=username)
                response = redirect('/employee/dashboard/')
                response.set_cookie('email', username)
                response.set_cookie('username',user.name)
                return response
            else:
                return render(request,'landing_page.html',{'error':'Invalid email or password'})
        except Exception as e:
            return render(request,'landing_page.html',{'error':'Internal Server Error'})
    return render(request,'landing_page.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')

        try:
            emp = Employee.objects.filter(email=email)
            if len(emp)==0:
                employee = Employee(
                name=name,email=email,password=sha256(password.encode('utf-8')).hexdigest(),
                phone_number=phone_number,date_of_birth=date_of_birth,address=address)
                employee.save()
                return redirect('')
            else:
                return render(request,'employee_register.html',{'error':'User Already Exists'})
            
        except Exception as e:
            print(e)
    return render(request,'employee_register.html')

def logout(request):
    response = redirect('/')
    response.delete_cookie('email')
    response.delete_cookie('username')
    return response

def dashboard(request):
    username = request.COOKIES.get('username') 
    noti = Notifications.objects.all().order_by('-id')
    return render(request,'employee_dashboard.html',{'name':username,'notifications':noti})

def view_salary(request):
    email = request.COOKIES.get('email') 
    emp_salary = EmployeeSalary.objects.filter(email=email)
    return render(request,'emp_view_salaries.html',{'salaries':emp_salary})

def viewholidays(request):
    email = request.COOKIES.get('email') 
    leave = LeaveRequest.objects.filter(email=email)
    leave_count = RemainLeave.objects.filter(email=email)
    to = 0
    try:
        for x in leave_count:
            to+=int(x.total_leave)
    except:
        pass
    return render(request,'view_holidays.html',{'leave_status':leave,'total':to})

def applyforleave(request):
    if request.method=='POST':
        email = request.COOKIES.get('email') 
        username = request.COOKIES.get('username') 
        reason =request.POST.get('reason')
        startdate =request.POST.get('start_date')
        enddate =request.POST.get('end_date')
        if enddate<startdate:
            return render(request,'emp_apply_for_leave.html',{'error':'Invalid Dates'})
        try:
            leave =LeaveRequest(email=email,username=username,reason=reason,leave_date_from=startdate,leave_date_to=enddate)
            leave.save()

            return redirect('/employee/dashboard/')
        except Exception as e:print(e)
    return render(request,'emp_apply_for_leave.html')

