from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.home, name='index'),
    path("home.html", views.contact, name="home"),
    path("shop.html", views.shop, name="shop"),
    path("shop", views.shop, name="shop"),
    path("contact", views.contact, name="contact"),
    path("contact", views.registemessage, name="contact"),
    path("login_view", views.login_view, name="login_view"),
    
    # Use LogoutView here
    path("logout", views.logout_view, name="logout"),
    
    path("blog.html", views.blog, name="blog"),
    path("about", views.about, name="about"),
    path("about.html", views.about, name="about"),
    path("vagetables", views.vegg, name="vagetables"),
    path("vagetables.html", views.vegg, name="vagetables"),
    path("test2", views.test2, name="test2"),
    path("register", views.register, name="register"),
    path("regapi", views.reg, name="regapi"),
    path("dashbord", views.dashbord, name="dashbord"),
    path("api/vegs/<int:veg_id>/", views.veg_details),
    path('user/commande/create/', views.commande_view, name='create_commande'),
    path("commande/id/<int:commande_id>/", views.commande_detail, name="commande_detail"),
    path("vendeuse/dashbord/", views.dashboardven, name="dashven"),
    path('admin/', admin.site.urls),
    path('vegetables/create/', views.create_vegetable, name='create_vegetable'),
    path('vegetables/id/<int:id_veg>/', views.delete_veg, name='delete_veg'),
]
