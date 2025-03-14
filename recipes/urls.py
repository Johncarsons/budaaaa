from django.urls import path
from .views import signup_view, login_view, logout_view, recipe_list, recipe_create, recipe_edit, recipe_delete

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', recipe_list, name='recipe_list'),
    path('create/', recipe_create, name='recipe_create'),
    path('edit/<int:pk>/', recipe_edit, name='recipe_edit'),
    path('delete/<int:pk>/', recipe_delete, name='recipe_delete'),
]
