from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import MaterialForm
from user.models import User
from .models import Material
import datetime

from function.distribute import distance


def match_score1(form,i):
    score = 0
    prov1 = form.user.address.split(' ')[0]
    city1 = form.user.address.split(' ')[1]
    prov2 = i.user.address.split(' ')[0]
    city2 = i.user.address.split(' ')[1]
    if form.mname == i.mname:
        add_score = 1
    else:
        add_score = 0
            
    score = (1/(distance(prov1,city1,prov2,city2)+1))*1000 + (1/(abs(form.number-i.number)+1))*100 + (14-i.x3)*0.1 + add_score*500
    return score


def match_score2(form,i):
    score = 0
    prov1 = form.user.address.split(' ')[0]
    city1 = form.user.address.split(' ')[1]
    prov2 = i.user.address.split(' ')[0]
    city2 = i.user.address.split(' ')[1]
    if form.mname == i.mname:
        add_score = 1
    else:
        add_score = 0

    
    score = (1/(distance(prov1,city1,prov2,city2)+1))*1000 + (1/(abs(form.number-i.number)+1))*100 + add_score*500
    return score



def match_to_hospital(form,material_list):
    score = []
    for i in material_list:
        score.append(match_score1(form,i))
    material_match = material_list[0]
    score_max = score[0]
    for i in range(len(score)):
        if score[i] > score_max:
            score_max = score[i]
            material_match = material_list[i]
    return material_match

def match_to_bar(form,material_list):
    score = []
    for i in material_list:
        score.append(match_score2(form,i))
    material_match = material_list[0]
    score_max = score[0]
    for i in range(len(score)):
        if score[i] > score_max:
            score_max = score[i]
            material_match = material_list[i]
    return material_match




def add_new(request):
    if request.session.get('name') != None:
        if request.method == 'POST':
            form = MaterialForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = User.objects.get(name=request.session.get('name'))
                #物资自动匹配
                if form.user.is_hospital == False:
                    type_material = Material.objects.filter(type=form.type)
                    material_list = []
                    for i in type_material:
                        if i.user.is_hospital == True and i.is_match == False:
                            material_list.append(i)
                    if material_list:
                        get_hosiptal_material = match_to_hospital(form,material_list)
                        form.is_match = True
                        form.match_id = get_hosiptal_material.id
                        form.save()
                        get_hosiptal_material.is_match = True
                        get_hosiptal_material.match_id = form.id
                        get_hosiptal_material.save()
                    else:
                        pass
                    form.save()
                else:
                    type_material = Material.objects.filter(type=form.type)
                    material_list = []
                    for i in type_material:
                        if i.user.is_hospital == False and i.is_match == False:
                            material_list.append(i)
                    if material_list:
                        get_bar_material = match_to_bar(form,material_list)
                        form.is_match = True
                        form.match_id = get_bar_material.id
                        form.save()
                        get_bar_material.is_match = True
                        get_bar_material.match_id = form.id
                        get_bar_material.save()
                    else:
                        pass
                    form.save()

                return redirect(reverse('user:home'))
            else:
                user_object = request.session.get('name')
                if user_object:
                    material = User.objects.get(name=user_object).material_set.values()
                    is_hospital = User.objects.get(name=user_object).is_hospital
                    user = User.objects.get(name=user_object)
                    errors = '需求发布失败，请重新发布'
                    return render(request, 'home.html', {'name': user_object, 'material': material,'username': request.session.get('name'),
                                                         'is_hospital': is_hospital, 'user': user,'errors':errors})
                else:
                    return redirect(reverse('user:login'))
                # return redirect(reverse('user:home'))

                # errors = '发布需求失败,请重新发布需求'
                # response.set_cookie('errors',errors)
                # response.set_cookie('errortime',1)
                # return render(request, 'add_new.html', {'form': form,'username':request.session.get('name')})

        # else:
        #     form = MaterialForm()
        # return render(request,'add_new.html',{'form':form,'username':request.session.get('name')})
        return redirect(reverse('user:home'))

    else:
        return redirect(reverse('user:login'))

def edit_m(request,edit_id):
    if request.session.get('name') != None:
        edit_material = Material.objects.get(id=edit_id)
        user = User.objects.get(name=request.session.get('name'))
        if request.method == 'POST':
            form = MaterialForm(data=request.POST,instance=edit_material)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = User.objects.get(name=request.session.get('name'))
                form.save()
                return redirect(reverse('user:home'))
            else:
                is_hospital = User.objects.get(name=request.session.get('name')).is_hospital
                return render(request, 'edit_m.html', {'form': form, 'edit_id': edit_id,'username':request.session.get('name'),'user':user,'is_hospital':is_hospital})
        else:
            form = MaterialForm(instance=edit_material)
            is_hospital = User.objects.get(name=request.session.get('name')).is_hospital
        return render(request,'edit_m.html',{'form':form,'edit_id':edit_id,'username':request.session.get('name'),'user':user,'is_hospital':is_hospital})
    else:
        return redirect(reverse('user:login'))

def check(request,check_id):
    detail = Material.objects.get(id=check_id)
    if check_id < Material.objects.all().count():
        next_id = check_id+1
    else :
        next_id = Material.objects.all().count()

    if check_id > 2:
        last_id = check_id-1
    else:
        last_id = 2
    return render(request,'check.html',{'next_id':next_id,'detail':detail,'username':request.session.get('name'),'last_id':last_id})




def search_type(request):
    type = request.POST.get('search_type')
    a = Material.objects.filter(type=type).count()
    if a>=15:
        list = Material.objects.filter(type=type)[a-15:a]
    else:
        list = Material.objects.filter(type=type)[0:15]
    a = Material.objects.all().count()
    news = Material.objects.filter(id=a).first()

    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    yes_all = Material.objects.filter(is_match=True).count()
    no_all = a - yes_all
    if a != 0:
        p_all = str(yes_all / a * 100)[:4] + '%'
    else:
        p_all = "0 %"

    all_today = Material.objects.filter(add_date=now_time).count()
    yes_today = Material.objects.filter(is_match=True, add_date=now_time).count()
    no_today = all_today - yes_today
    if all_today != 0:
        p_today = str(yes_today / all_today * 100)[:4] + '%'
    else:
        p_today = "0 %"
    number_data = [yes_all, no_all, yes_today, no_today, p_all, p_today]
    return render(request,'index.html',{'list':list,'username':request.session.get('name'),'news':news,'number_data':number_data})

def search_is_hospital(request):
    is_hospital = request.POST.get('search_is_hospital')
    if is_hospital == 'True':
        k = True
    else:
        k = False
    list = []
    for i in Material.objects.all():
        if i.user.is_hospital == k :
            list.append(i)
    list = list[-15:]
    a = Material.objects.all().count()
    news = Material.objects.filter(id=a).first()

    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    yes_all = Material.objects.filter(is_match=True).count()
    no_all = a - yes_all
    if a != 0:
        p_all = str(yes_all / a * 100)[:4] + '%'
    else:
        p_all = "0 %"

    all_today = Material.objects.filter(add_date=now_time).count()
    yes_today = Material.objects.filter(is_match=True, add_date=now_time).count()
    no_today = all_today - yes_today
    if all_today != 0:
        p_today = str(yes_today / all_today * 100)[:4] + '%'
    else:
        p_today = "0 %"
    number_data = [yes_all, no_all, yes_today, no_today, p_all, p_today]
    return render(request,'index.html',{'list':list,'username':request.session.get('name'),'news':news,'number_data':number_data})



def match(request,m_id):
    mym = Material.objects.get(id=m_id)
    myobj = mym.user
    othermobj = Material.objects.get(id=mym.match_id)
    otherobj = othermobj.user
    is_hospital = User.objects.get(name=request.session.get('name')).is_hospital
    user = User.objects.get(name=request.session.get('name'))
    
    return render(request,'match.html',{'username':request.session.get('name'),'myobj':myobj,'otherobj':otherobj,'othermobj':othermobj,'is_hospital':is_hospital,'user':user})

def rematch(request,m_id):
    if request.session.get('name') != None:
        mym = Material.objects.get(id=m_id)
        otherm = Material.objects.get(id=mym.match_id)
        mym.is_match = False
        mym.match_id = -1
        otherm.is_match = False
        otherm.match_id = -1
        mym.save()
        otherm.save()
        return redirect(reverse('user:home'))
    else :
        return redirect(reverse('user:login'))

def match_list(request,user_id):
    user = User.objects.get(id=user_id)
    match_m = user.material_set.filter(is_match=True)
    to_m = []
    for i in match_m:
        to_m.append(Material.objects.get(id=i.match_id))
    bag = zip(match_m,to_m)
    return render(request,'match_list.html',{'username':request.session.get('name'),'is_hospital':user.is_hospital,'user':user,'bag':bag})
