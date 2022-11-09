from django.urls import path
from django.views import View
from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('restaurents',views.restaurents, name='restaurents'),
    path('about_us',views.about_us, name='about_us'),
    path('partner', views.partner, name='partner'),
    path('job', views.jobs, name='job'),
    path('stories', views.stories, name='stories'),
    path('register', views.register, name='register'),
    path('menu/<rid>',views.menu_, name='menu'),
    path('bill',views.bill_,name="bill"),
    path('login', views.login_user, name='login'),
    path('logout',views.logout_use, name='logout'),
    path('confirmed', views.confirmed, name='confirmed'),
    path('Myorders', views.myorders, name='Myorders'),
    path('Menu_list',views.menu_list, name='Menu_list'),
    path('del/<m_id>',views.delete_menu, name='del'),
    path('update/<m_id>', views.menu_edit, name='update'),
    path('order_list',views.order_list, name='order_list'),
    path('order_list_del',views.order_list_del, name='order_list_del')
]