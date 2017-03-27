from django.forms import ModelForm
from douban.models import Douban


class DoubanForm(ModelForm):
    class Meta:
        model = Douban
        fields = ['title', 'rate', 'region', 'run_time']
