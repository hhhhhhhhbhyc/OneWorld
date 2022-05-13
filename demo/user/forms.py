from django.forms import Form,ModelForm
from django import forms
from .models import User
from django.utils.translation import gettext_lazy as _

class UserForm(ModelForm):
    password2 = forms.CharField(label="确认密码",max_length=256,widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['name','password','password2','phone_number','address','linkman','is_hospital']
        labels = {
            'name': _('用户名'),
            'password': _('密码'),
            'password2': _('确认密码'),
            'phone_number': _('联系电话'),
            'address': _('地址'),
            'linkman': _('联系人'),
            'is_hospital': _('是否为医院'),
        }
        error_messages = {
            'name': {
                'max_length': _("用户名太长"),
                'min_length': _('用户名太短'),
            },
            'password': {
                'max_length': _("密码太长"),
            },
            'password2': {
                'max_length': _("密码太长"),
            },
            'phone_number': {
                'max_length': _("电话号码太长"),
            },
            'address': {
                'max_length': _("地址太长"),
            },
            'linkman': {
                'max_length': _("联系人错误"),
            },
        }
        widget = {
            'password':forms.PasswordInput(),
            'password2':forms.PasswordInput(),
        }









# name = forms.CharField(label="用户名",max_length=20,min_length=3,required=True)
# password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput())
# password2 = forms.CharField(label="确认密码", max_length=256,widget=forms.PasswordInput())
# phone_number = forms.CharField(label='联系电话',max_length=12)
# address = forms.CharField(label='地址',max_length=256)
# linkman = forms.CharField(label='联系人姓名',max_length=5)
# is_hospital = forms.BooleanField(label='是否为医院')

