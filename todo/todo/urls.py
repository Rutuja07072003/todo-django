from . import views
from django.contrib import admin
from django.urls import path ,include

from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),  # Added 'name' for reverse
    path('loginn/', views.loginn, name='loginn'),  # Added 'name' for reverse
    path('todopage/', views.todo, name='todo'),  # Added 'name' for reverse
    path('delete_todo/<int:srno>/', views.delete_todo, name='delete_todo'),  # Added trailing slash and 'name'
    path('edit_todo/<int:srno>/', views.edit_todo, name='edit_todo'),  # Added 'name' for reverse
    path('signout/', views.signout, name='signout'),  # Added 'name' for reverse
]


