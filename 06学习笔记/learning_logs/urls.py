"""定义learning_logs的URL模式"""

from django.urls import path
from . import views

urlpattens = {
    # 主页
    path(r'^$', views.index, name='index')
}
