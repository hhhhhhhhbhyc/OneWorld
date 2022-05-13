"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.shortcuts import render
from material.models import Material
import datetime


from django.views.static import serve

from .settings import  STATIC_ROOT


def index(request):
    a = Material.objects.all().count()
    if a <16:
        material_list = Material.objects.all()
    else:
        material_list = Material.objects.all()[a-15:a]
    news = Material.objects.filter(id=a).first()

    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    yes_all = Material.objects.filter(is_match=True).count()
    no_all = a - yes_all
    if a != 0:
        p_all = str(yes_all/a*100)[:4] + '%'
    else:
        p_all = "0 %"

    all_today = Material.objects.filter(add_date=now_time).count()
    yes_today = Material.objects.filter(is_match=True,add_date=now_time).count()
    no_today = all_today - yes_today
    if all_today != 0:
        p_today = str(yes_today /all_today*100)[:4] + '%'
    else:
        p_today = "0 %"
    number_data = [yes_all,no_all,yes_today,no_today,p_all,p_today]
    return render(request,'index.html',{'list':material_list,'username':request.session.get('name'),'news':news,'number_data':number_data})

def help(request):
    return render(request,'help.html',{'username':request.session.get('name')})


# def test(request):
#     return render(request,'test.html')


def map(request):
    return render(request,'map_origin.html')

def picture(request):
    return render(request,'day_public_match.html')

from function.pathdraw import distance3,solve,find_fuc
from pyecharts import options as opts
from pyecharts.charts import Map3D
from pyecharts.globals import ChartType

def data_tranfer(x):
    jingdu = []
    weidu = []
    for citt in x:
        jingdu.append(float(citt[2]))
        weidu.append(float(citt[3]))
    jingweidu = list(zip(jingdu, weidu))
    # print(jingweidu)
    example_data = [[jingweidu[i], jingweidu[i + 1]] for i in range(len(jingweidu) - 1)]
    # print(example_data)
    c = (
        Map3D()
            .add_schema(

            itemstyle_opts=opts.ItemStyleOpts(
                color="rgb(5,101,123)",
                opacity=1,
                border_width=0.8,
                border_color="rgb(62,215,213)",
            ),
            light_opts=opts.Map3DLightOpts(
                main_color="#fff",
                main_intensity=1.2,
                is_main_shadow=False,
                main_alpha=55,
                main_beta=10,
                ambient_intensity=0.3,
            ),
            view_control_opts=opts.Map3DViewControlOpts(center=[-10, 0, 10]),
            post_effect_opts=opts.Map3DPostEffectOpts(is_enable=False),
        )
            .add(
            series_name="",
            data_pair=example_data,
            type_=ChartType.LINES3D,
            effect=opts.Lines3DEffectOpts(
                is_show=True,
                period=0.6,
                trail_width=7.6,
                trail_length=1.8,
                trail_color="#f00",
                trail_opacity=1,
            ),
            linestyle_opts=opts.LineStyleOpts(is_show=False, color="#fff", opacity=0),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="路径规划可视化"))
            .render("templates/routeline.html")
    )



def pathdraw(request,m_id):
    mym = Material.objects.get(id=m_id)
    myobj = mym.user
    othermobj = Material.objects.get(id=mym.match_id)
    otherobj = othermobj.user
    an = myobj.address.split(' ')[1]
    bn = otherobj.address.split(' ')[1]

    a = find_fuc(an)
    b = find_fuc(bn)
    main_list = solve(a, b)
    data_tranfer(main_list)
    print("draw map successfully")
    return render(request,'routeline.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('user.urls')),
    path('index/',index,name='index'),
    path('material/',include('material.urls')),
    path('help/',help,name='help'),
    # path('test/',test,name='test'),
    path('map/',map,name='map'),
    path('picture/',picture,name='picture'),
    path('',index),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    path('pathdraw/<int:m_id>/',pathdraw,name='pathdraw'),
]
