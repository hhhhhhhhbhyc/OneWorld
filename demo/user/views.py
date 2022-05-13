from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import UserForm
from .models import User
from material.models import Material

from function import province

import sys
sys.path.append('../')
# Create your views here.

# username = request.session.get('name')

def register(request):
    if request.method == 'POST':
        #处理request.post中的城市，将数值改为对应城市字符串
        num = int(request.POST.get('province'))
        # print(num)
        prov = province.provinceArr[num]
        # print(prov)
        city = request.POST.get('city')
        # print(city)

        data = {'name':request.POST.get('name'),'password':request.POST.get('password'),'password2':request.POST.get('password2'),
                'phone_number':request.POST.get('phone_number'),'address':prov+" "+city,
                'linkman':request.POST.get('linkman'),'is_hospital':request.POST.get('is_hospital')}
        form = UserForm(data=data)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password2']:
                form.save()
                request.session['name'] = form.cleaned_data['name']
                return redirect(reverse('user:home'))
            else:
                msg = '注册失败'
                return render(request, 'register.html', {'form': form,'msg':msg,'username':request.session.get('name')})
        else:
            return render(request,'register.html',{'form':form,'username':request.session.get('name')})
    else:
        form = UserForm()
    return render(request,'register.html',{'form':form,'username':request.session.get('name')})

def login(request):
    if request.method == 'POST':
        login_user = request.POST.get('name')
        login_password = request.POST.get('password')
        login_object = User.objects.filter(name=login_user,password=login_password).first()
        if login_object:
            request.session['name'] = login_object.name
            return redirect(reverse('user:home'))
        else:
            form = UserForm(request.POST)
            msg ='用户名或密码错误'
        return render(request,'login.html',{'form':form,'msg':msg,'username':request.session.get('name')})
    else:
        form = UserForm()
    return render(request,'login.html',{'form':form,'username':request.session.get('name')})

def home(request):
    user_object = request.session.get('name')
    if user_object:
        material = User.objects.get(name=user_object).material_set.values()
        is_hospital = User.objects.get(name=user_object).is_hospital
        user = User.objects.get(name=user_object)
        response = render(request,'home.html',{'name':user_object,'material':material,'username':request.session.get('name'),'is_hospital':is_hospital,'user':user})
        return response
    else:
        return redirect(reverse('user:login'))

def logout(request):
    del request.session['name']
    return redirect(reverse('index'))


def test(request):
    return render(request,'test.html',{'username':request.session.get('name'),'user':user,'is_hospital':user.is_hospital})

def test_password(request,user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        if user.password == request.POST.get('password_first'):
            return redirect(reverse('user:edit_info',kwargs={'user_id':user_id}))
    if request.session.get('name') != None:
        user = User.objects.get(id=user_id)
        passworderror = "输入密码错误,请重新输入"
        return render(request,'user_info.html',{'username':request.session.get('name'),'user':user,'is_hospital':user.is_hospital,'passworderror':passworderror})
    else:
        return redirect(reverse('user:login'))


def edit_info(request,user_id):
    if request.session.get('name') != None:
        if request.method == 'POST':
            edit_user = User.objects.get(id=user_id)
            # 处理request.post中的城市，将数值改为对应城市字符串
            num = int(request.POST.get('province'))
            prov = province.provinceArr[num]
            city = request.POST.get('city')

            data = {'name': request.POST.get('name'), 'password': request.POST.get('password'),
                    'password2': request.POST.get('password2'),
                    'phone_number': request.POST.get('phone_number'),
                    'address': prov+" "+city,
                    'linkman': request.POST.get('linkman'), 'is_hospital': request.POST.get('is_hospital')}
            form = UserForm(data=data,instance=edit_user)
            if form.is_valid():
                form.save()
                return redirect(reverse('user:home'))
            else:
                # ErrorDict = form.errors
                # print(type(ErrorDict))
                # print(ErrorDict)
                return redirect(reverse('index'))
        else:
            user = User.objects.get(id=user_id)
            is_hospital = User.objects.get(name=request.session.get('name')).is_hospital
            return render(request,'edit_info.html',{'username':request.session.get('name'),'user':user,'is_hospital':is_hospital})
    else:
        return redirect(reverse('user:login'))

def user_info(request,user_id):
    if request.session.get('name') != None:
        user = User.objects.get(id=user_id)
        return render(request,'user_info.html',{'username':request.session.get('name'),'user':user,'is_hospital':user.is_hospital})
    else:
        return redirect(reverse('user:login'))

def picture(request,user_id):
    if request.session.get('name') != None:
        user = User.objects.get(id=user_id)

        import pyecharts.options as opts
        from pyecharts.charts import Line
        import datetime

        # dic_all = {'day1': [3, 14], 'day2': [5, 54], 'day3': [0, 5], 'day4': [13, 24], 'day5': [13, 4]}

        user_materal_list = User.objects.get(id=user_id).material_set.all()

        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        all_today = user_materal_list.filter(add_date=now_time).count()
        yes_today = user_materal_list.filter(is_match=True, add_date=now_time).count()

        yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
        all_yesterday = user_materal_list.filter(add_date=yesterday).count()
        yes_yesterday = user_materal_list.filter(is_match=True, add_date=yesterday).count()

        day3 = (datetime.datetime.now() + datetime.timedelta(days=-2)).strftime("%Y-%m-%d")
        all_day3 = user_materal_list.filter(add_date=day3).count()
        yes_day3 = user_materal_list.filter(is_match=True, add_date=day3).count()

        day4 = (datetime.datetime.now() + datetime.timedelta(days=-3)).strftime("%Y-%m-%d")
        all_day4 = user_materal_list.filter(add_date=day4).count()
        yes_day4 = user_materal_list.filter(is_match=True, add_date=day4).count()


        day5 = (datetime.datetime.now() + datetime.timedelta(days=-4)).strftime("%Y-%m-%d")
        all_day5 = user_materal_list.filter(add_date=day5).count()
        yes_day5 = user_materal_list.filter(is_match=True, add_date=day5).count()

        dic_all = {}
        dic_all["5天前"] = [all_day5,yes_day5]
        dic_all["4天前"] = [all_day4,yes_day4]
        dic_all['前天'] = [all_day3,yes_day3]
        dic_all['昨天'] = [all_yesterday, yes_yesterday]
        dic_all['今天'] = [all_today,yes_today]

        public_num = []
        match_num = []
        day = list(dic_all.keys())
        for i in list(dic_all.values()):
            public_num.append(i[0])
            match_num.append(i[1])

        (
            Line(init_opts=opts.InitOpts(width="1100px", height="650px"))
                .add_xaxis(xaxis_data=day)
                .add_yaxis(
                series_name="发布数",
                y_axis=public_num, is_smooth=True,
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="最大值"),
                        opts.MarkPointItem(type_="min", name="最小值"),
                    ]
                ),
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(type_="average", name="平均值")]
                ),
                areastyle_opts=opts.AreaStyleOpts(opacity=0.4, color="#808000")
            )
                .add_yaxis(
                series_name="匹配数",
                y_axis=match_num, is_smooth=True,

                markline_opts=opts.MarkLineOpts(
                    data=[
                        opts.MarkLineItem(type_="average", name="平均值"),
                        opts.MarkLineItem(symbol="none", x="90%", y="max"),
                        opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
                    ]
                ),
                areastyle_opts=opts.AreaStyleOpts(opacity=0.4, color="#6A5ACD")
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="个人中心数据统计", subtitle="发布＆匹配",
                                          title_textstyle_opts=(opts.TextStyleOpts(color='white',font_size=20)),subtitle_textstyle_opts=(opts.TextStyleOpts(font_size=16)),),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                toolbox_opts=opts.ToolboxOpts(is_show=True),
                xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
                legend_opts=opts.LegendOpts(
                    textstyle_opts=opts.TextStyleOpts(color='rgba(55,254,253,0.3)', font_size=18),

                ),
            )
                .render("templates/day_public_match.html")
        )

        return render(request,'picture.html',{'username':request.session.get('name'),'user':user,'is_hospital':user.is_hospital})
    else:
        return redirect(reverse('user:login'))



from pyecharts.charts import Map
from pyecharts import options as opts
import time

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

#开启定时工作
try:
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # 设置定时任务，选择方式为interval，时间间隔为10s
    # 另一种方式为每天固定时间执行任务，对应代码为：
    # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
    @register_job(scheduler,"interval", seconds=600)
    def my_job():
        date = time.strftime("%Y年%m月%d日")
        # print(date)
        rscname = "物资"
        rsctype = "需求"  # 这里根据用户在网页上的选择来定义数值，可以先默认一个显示数值
        # 省和直辖市

        province_distribution = {'湖北': 0, '浙江': 0, '广东': 0,
                                 '湖南': 0, '河南': 0, '安徽': 0,
                                 '重庆': 0, '山东': 0, '江西': 0,
                                 '四川': 0, '江苏': 0, '北京': 0,
                                 '福建': 0, '上海': 0, '广西': 0,
                                 '陕西': 0, '河北': 0, '云南': 0,
                                 '海南': 0, '黑龙江': 0, '辽宁': 0,
                                 '山西': 0, '天津': 0, '甘肃': 0,
                                 '内蒙古': 0, '新疆': 0, '宁夏': 0,
                                 '贵州': 0, '吉林': 0, '台湾': 0,
                                 '香港': 0, '澳门': 0, '青海': 0,
                                 '西藏': 0,
                                 }

        for i in Material.objects.all():
            if i.user.is_hospital == True:
                prov = i.user.address.split(' ')[0]
                if '黑龙江' in prov or '内蒙古' in prov:
                    prov = prov[0:3]
                else:
                    prov = prov[0:2]
                province_distribution[prov] += i.number

        # maptype='china' 只显示全国直辖市和省级
        map = Map()
        map.set_global_opts(
            title_opts=opts.TitleOpts(title=date + "需求总览",title_textstyle_opts=(opts.TextStyleOpts(color='white',font_size=20)),),  # 获取当日日期
            visualmap_opts=opts.VisualMapOpts(max_=3600, is_piecewise=True,textstyle_opts=opts.TextStyleOpts(color='white', font_size=16),
                                              pieces=[
                                                  {"max": 100000, "min": 5001, "label": ">5000", "color": "#8A0808"},
                                                  {"max": 5000, "min": 2000, "label": "2000-5000", "color": "#B40404"},
                                                  {"max": 1999, "min": 1000, "label": "1000-1999", "color": "#DF0101"},
                                                  {"max": 999, "min": 100, "label": "100-999", "color": "#F78181"},
                                                  {"max": 99, "min": 1, "label": "1-99", "color": "#F5A9A9"},
                                                  {"max": 0, "min": 0, "label": "0", "color": "#FFFFFF"},
                                              ], ) , # 最大数据范围，分段
            legend_opts=opts.LegendOpts(
                textstyle_opts=opts.TextStyleOpts(color='white', font_size=18),

            ),
        )
        map.add(rscname + rsctype , data_pair=province_distribution.items(), maptype="china", is_roam=True)
        map.render('templates/map_origin.html')
        print("update successful.")
    register_events(scheduler)
    scheduler.start()
except Exception as e:
    print(e)
    # 有错误就停止定时器
    # scheduler.shutdown()
