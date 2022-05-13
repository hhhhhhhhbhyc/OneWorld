from django.forms import Form,ModelForm
from django import forms
from .models import Material
from django.utils.translation import gettext_lazy as _

class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ['mname','type','number','x1','x2','x3','postscript']
        labels = {
            'mname': _('物资名称'),
            'postscript': _('备注'),
            'number': _('数量'),
            'type': _('物资类型'),
            'x1': _('当前患者人数'),
            'x2': _('当前医护人数'),
            'x3': _('紧急日期天数'),
        }
        error_messages = {
            'mname': {
                'max_length': _("物资名太长"),
            },
            'postscripts': {
                'max_length': _("备注太长"),
            },

            'type': {
                'max_length': _("类型错误"),
            },

        }
