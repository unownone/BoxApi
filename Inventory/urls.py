from django.urls import path
from Inventory import views

urlpatterns = [
    path('list/', views.list_boxes),
    path('list/<str:uname>/', views.list_boxes),
    path('add/',views.add_box),
]