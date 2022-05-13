from django.urls import path,include
from . import views

#应用命名空间
app_name = 'user'

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('home/',views.home,name='home'),
    path('logout/',views.logout,name='logout'),
    path('edit_info/<int:user_id>/', views.edit_info, name='edit_info'),
    path('user_info/<int:user_id>/',views.user_info,name='user_info'),
    path('test_password/<int:user_id>/',views.test_password,name='test_password'),
    path('picture/<int:user_id>/',views.picture,name='picture'),
    path('test/',views.test,name='test'),

]
