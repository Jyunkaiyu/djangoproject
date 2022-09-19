from django.urls import path,re_path
from . import views
from django.contrib.auth import views as auth_views
# url(r'^blog/(?P<blog_id>\d+)/$'
urlpatterns = [
    path('',views.index,name='index'),
    # path('<gender>/', views.index, name='first1'),
    path('add/', views.add, name='add_members'),
    path('add/add_record/', views.add_record, name='add_record'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('test1/', views.test1, name='test'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register_User, name='register'),    
    path('profile/<str:pk>', views.profile, name='profile'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('add_product/',views.add_product,name='add_product'),
    path('shopping_cart/',views.shopping_carts,name='shopping_cart'),
    path('delete_product/<int:pk>',views.delete_product,name='delete_product'),
    path('add_product2/',views.add_product2,name='add_product2'),
    path('home/',views.home,name='home'),
    path('login1/',views.login1,name='login1'),
    path('member_centre/',views.member_center,name='member_centre'),
    path('member_profile/',views.member_profile,name='member_profile'),
    path('product/<str:pk>', views.product_page, name='product'),
    path('buy/',views.buy,name='buy'),
    path('category/<str:pk>/',views.category,name='category'),
    path('purchase_record/',views.purchase_record,name='purchase_record'),
]