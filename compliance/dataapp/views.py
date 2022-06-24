from calendar import c
import json
import numbers
import string
from django.shortcuts import render, redirect,  get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserForm, PostForm, RegisterForm
from .models import Post, Problem, ProblemEncoder, User, Operation
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from slugify import slugify
import pandas as pd
import openpyxl
import os, math
from json import dumps

# Create your views here.



def index(request):
    return render(request, 'index.html', locals())



def login(request):
    print(request.session.get('is_login', None))
    if request.session.get('is_login', None):
        return redirect('dataapp:index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    return redirect('dataapp:post_list')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())

    login_form = UserForm()
    return render(request, 'login.html', locals())


def register(request):

    if request.session.get('is_login', None):
        # 登录状态不允许注册
        return redirect("dataapp:index")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        print(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = User.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = User.objects.create()
                new_user.username = username
                new_user.password = password1
                new_user.email = email
                # new_user.sex = sex
                new_user.save()
                return redirect('dataapp:login')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('dataapp:index')
    request.session.flush()

    return redirect('dataapp:index')




def post_list(request):
    if not request.session.get('is_login', None):
        # 非登录状态显示主页
        return redirect("dataapp:index")
    user = User.objects.filter(username=request.session['user_name']).first() 
    posts = user.user_posts.all()
    # for post in posts:
        # print(post)
        # print(post.get_absolute_url())
    return render(request,'post_list.html',{'posts':posts})


class MainView(TemplateView):
    template_name = 'dataapp/main.html'

def file_upload_view(request):
    print(request.FILES)
    print(request.POST)
    print(request.POST.get('title'))
    print(request.POST.get('body'))
    print(request.FILES.get('file[0]'))
    print(request.session['user_name'])

    
    if not request.session.get('is_login', None):
        # 非登录状态显示主页
        return redirect("dataapp:index")

    if request.method == "POST":

        myfile={'upload':request.FILES.get('file[0]')}
        the_user=User.objects.get(username=request.session['user_name'])
        my_request=request.POST.copy()
        my_request['author']=the_user.id

        post_form = PostForm(my_request, myfile)
        message = "请检查填写的内容！"
        if post_form.is_valid():
            title = post_form.cleaned_data['title']
            same_name_title = Post.objects.filter(title=title)
            if same_name_title:
                print('项目已经存在')
                message = '项目已经存在，请重新选择项目名称！'
                return render(request, 'new_post.html', locals())
            post_form.cleaned_data['slug'] = slugify(post_form.cleaned_data['title'])

            attachment = post_form.save()
            #为新增的数据添加slug
            new_post = Post.objects.filter(title=post_form.cleaned_data['title']).get()
            new_post.slug = slugify(post_form.cleaned_data['title'])
            new_post.save()
            print('项目添加成功')

            data = {'is_valid':True, 'url':attachment.upload.url, 'name':attachment.upload.name}

            return redirect("dataapp:post_list") 
    post_form = PostForm()
    if request.method == 'GET':
        return render(request,"new_post.html")

       


def post_detail(request, post):
    post=get_object_or_404(Post,slug=post)
    path ='media/'+str(post.upload)
    all_data=pd.read_csv(path)
    number_per_page=15
    if request.GET.get('high_level_handle_time')==None:
        data = all_data.sample(n=40)
        

    # 如果点击高风险数据处理
    if request.GET.get('high_level_handle_time'):
        all_data.loc[[not str(i).count('*') for i in all_data['phone_number']],'phone_number']=all_data.loc[[not str(i).count('*') for i in all_data['phone_number']],'phone_number'].astype(str).str[0:3] + '****' +all_data.loc[[not str(i).count('*') for i in all_data['phone_number']],'phone_number'].astype(str).str[7:]
        data = all_data.sample(n=40)
        print('高风险数处理时间',request.GET.get('high_level_handle_time'))

   
    # if os.path.splitext(path)[-1]=='.csv':
    # 将数据转换成列表，以便前端读取
    table_head = list(data.columns)
    excel_data = list()
    for row in range(data.shape[0]):
        excel_data.append(list(data.iloc[row]))

    # 将数据分页展示
    paginator = Paginator(excel_data, number_per_page) # 每页15条数据
    page = request.GET.get('page')
   
    try:
        excel_data = paginator.page(page)
    except PageNotAnInteger:
        excel_data = paginator.page(1)
    except EmptyPage:
        excel_data = paginator.page(paginator.num_pages)
        

    # 找出高风险数据
    step=number_per_page
    data_slice = [data[i:i+step] for i in range(0,len(data),step)]  #分页查找
    high_level={}
    for p in range(len(data_slice)+1):
        if page==None:
            page=1    
        if p == int(page)-1:
            cols=list(data_slice[p])
            high_level_cols=['name','phone_number']
            # data_slice[p]['phone_number']=data_slice[p]['phone_number'].astype(str)
            for col in high_level_cols:
                if col in cols:
                    for item in list(data_slice[p][col]):
                        if not item.count('*'):
                            if not list(data_slice[p][col]).index(item) in high_level.keys():
                                high_level[list(data_slice[p][col]).index(item)]=[cols.index(col),]
                            else:
                                high_level[list(data_slice[p][col]).index(item)].append(cols.index(col))

    # 找出中风险数据
    middle_level={}
    for p in range(len(data_slice)+1):
        if page==None:
            page=1    
        if p == int(page)-1:
            cols=list(data_slice[p])
            middle_level_cols=['address']
            for col in middle_level_cols:
                if col in cols:
                    for item in list(data_slice[p][col]):
                        if not item.count('*'):
                            if not list(data_slice[p][col]).index(item) in middle_level.keys():
                                middle_level[list(data_slice[p][col]).index(item)]=[cols.index(col),]
                            else:
                                middle_level[list(data_slice[p][col]).index(item)].append(cols.index(col))

    dataJSON_middle = dumps(middle_level)
    dataJSON = dumps(high_level)
    print('高风险',high_level)
    print('中风险',middle_level)
    




    return render(request, 'post_detail.html',{'post':post,'excel_data':excel_data, 
                                    page:'pages', 'data':dataJSON ,'middle_data':dataJSON_middle,'table_head':table_head})



def handle_high_level(request, post):
    post = get_object_or_404(Post,slug=post)
    path ='media/'+str(post.upload)
    all_data=pd.read_csv(path)
    all_data.loc[[not str(i).count('*') for i in all_data['phone_number']],'phone_number']=all_data.loc[[not str(i).count('*') for i in all_data['phone_number']],'phone_number'].astype(str).str[0:3] + '****' +all_data.loc[[not str(i).count('*') for i in all_data['phone_number']],'phone_number'].astype(str).str[7:]
    data = all_data.sample(n=40)
    number_per_page=15
   
    # if os.path.splitext(path)[-1]=='.csv':
    # 将数据转换成列表，以便前端读取
    table_head = list(data.columns)
    excel_data = list()
    for row in range(data.shape[0]):
        excel_data.append(list(data.iloc[row]))

    # 将数据分页展示
    paginator = Paginator(excel_data, number_per_page) # 每页15条数据
    page = request.GET.get('page')
   
    try:
        excel_data = paginator.page(page)
    except PageNotAnInteger:
        excel_data = paginator.page(1)
    except EmptyPage:
        excel_data = paginator.page(paginator.num_pages)

    return render(request, 'post_detail.html',{'post':post,'excel_data':excel_data, page:'pages','table_head':table_head})
                                    
    
 




def post_delete(requst,pk):
    post=Post.objects.get(id=pk)
    post.delete()
    return redirect("dataapp:post_list")



def generate_report(request,post):
    post=get_object_or_404(Post,slug=post)
    return render(request,"generate_report.html",{'post':post})


def UploadText(request):
    if request.method != "POST":
        return JsonResponse({'msg':'BAD request'})
    content = json.loads(request.body)
    content = content['data']
    newcontent = []
    print(type(content[0]))
    index = 0
    for row in content:
        [newrow,index] = HandleRow(row,index)
        newcontent.append(newrow)
    return JsonResponse({"data":newcontent})

def HandleRow(row,index):
    newrow = row.copy()
    problems = []

    # 处理名字
    nameresp = []
    if 'name' in row:
        nameresp = HandleName(row['name'],index+len(problems))
    else:
        nameresp = HandleName("",index+len(problems))
    problems.extend(nameresp)

    # 处理电话
    phoneresp = []
    if 'phone' in row:
        phoneresp = HandlePhone(row['phone'],index+len(problems))
    else:
        phoneresp = HandlePhone("",index+len(problems))
    problems.extend(phoneresp)

    # 处理address问题
    addressresp = []
    if 'address' in row:
        addressresp = HandleAddress(row['address'],index+len(problems))
    else:
        addressresp = HandleAddress("",index+len(problems))
    problems.extend(addressresp)

    # id问题
    idresp = []
    if 'ID' in row:
        idresp = HandleId(row['ID'],index+len(problems))
    else:
        idresp = HandleId("",index+len(problems))
    problems.extend(idresp)



    newrow['problems'] = problemencode(problems)
    index += len(problems)

    return [newrow,index]

# 处理名字
def HandleName(name,index):
    # 名字问题
    problems = []
    print(len(name))
    if len(name) <= 0:
        problems.append(Problem(index+len(problems),"Name","normal","完整性","缺少姓名信息",""))
        return problems
    # print(problems[0].description,flush=True)
    # 名字隐私性
    count = name.count("*")
    firstindex = name.find('*')
    # 有隐蔽，没问题
    if count > 0 and firstindex > 0:
        return problems
    
    #隐蔽性出现问题，构建新的name
    newname = ""
    newname += name[0]
    newname += '*'
    if len(name) > 2:
        newname = newname + name[-1]
    problems.append(Problem(index+len(problems),"Name","risky","隐私性","具体姓名需要隐去",newname))
    print(problems[0].pid)
    return problems

#处理电话
def HandlePhone(phone,index):
    # 电话问题
    problems = []
    # 电话缺失
    if len(phone) == 0:
        problems.append(Problem(index+len(problems),"Phone","caution","完整性","缺少电话信息",""))
        return problems
    
    # 电话位数
    if len(problems) != 11:
        problems.append(Problem(index+len(problems),"Phone","critical","规范性","phone格式与常规不符,且具体电话号码需隐去"))
        return problems
    
    # 电话隐私问题
    # 找****的位置
    # 找是否有****
    count = phone.count("****")
    firstindex = phone.find("****")
    cnt = phone.count("*")

    # 没有隐私问题
    if count == 1 and firstindex == 3:
        return problems

    if cnt != 0:
        problems.append(Problem(index+len(problems),"Phone","risky","规范性","phone的加密格式不对,有泄露隐私风险")) 
        return problems

    #没有加密，生成正确phone
    newphone = phone[0:3] + "****" + phone[7:] 
    problems.append(Problem(index+len(problems),"Phone","critical","隐私性","根据国家法律法规,具体电话号码需要加密",newphone))

    return problems  

# 处理地址问题
def HandleAddress(address,index):
    # 地址问题处理
    problems = []

    # 地址缺失
    if len(address) == 0:
        problems.append(Problem(index+len(problems),"Address","caution","完整性","缺少地址信息",""))
        return problems
    
    if len(address) <= 6:
        problems.append(Problem(index+len(problems),"Address","caution","完整性","缺少完整的地址信息"))
        return problems

    # 地址隐私问题
    count = address.count("****")
    firstindex = address.find("****")
    cnt = address.count("*")

    if count == 1 and firstindex == len(address) - 4:
        return problems
    
    if cnt != 0:
        problems.append(Problem(index+len(problems),"Address","caution","规范性","address的加密格式不对,需加密具体门牌"))
        return problems
    
    # address没加隐私
    # 正确的address加密格式
    newaddress = address[0:len(address)-6] + "****"
    problems.append(Problem(index+len(problems),"Address","critical","隐私性","具体门牌号可能带来风险,建议隐去",newaddress))

    return problems

# 处理id问题
def HandleId(pid,index):
    # id问题
    problems = []

    # 缺少身份证信息
    if len(pid) == 0:
        problems.append(Problem(index+len(problems),"ID","risky","完整性","缺少身份证信息"))
        return problems

    # 身份证位数不对
    if len(pid) != 18:
        problems.append(Problem(index+len(problems),"ID","caution","规范性","身份证格式与常规格式不符"))
        return problems
    
    # 身份证隐私问题
    count = pid.count("********")
    firstindex = pid.find("********")
    cnt = pid.count("*")

    # 没有问题
    if count == 1 and firstindex == 6 and cnt == 8:
        return problems

    if cnt != 0:
        problems.append(Problem(index+len(problems),"ID","caution","规范性","身份证加密格式不正确,有安全风险"))
        return problems

    newid = pid[0:6] + "********" + pid[14:]
    problems.append(Problem(index+len(problems),"ID","critical","隐私性","根据国家法律法规,身份证信息需要隐去",newid)) 
    
    return problems   

def problemencode(problems):
    newproblems = []
    for p in problems:
        print(p.__dict__)
        newproblems.append(p.__dict__)
        # newproblems.append(ProblemEncoder().encode(p))
    return newproblems