from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Recipe
from .forms import RecipeForm

# User Authentication Views
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipe_list')  # Redirect to viewing page
        else:
            print("signup invallid")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                print("logged in")
                return redirect('recipe_list')
            else:
                print("User not found")
        else:
            print("Invalid username or password")
            print(form.errors)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# Recipe Views
@login_required
def recipe_list(request):
    """ Show all recipes, if none exist, show 'Create a Recipe' button. """

    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'list.html', {'recipes': recipes})

@login_required
def recipe_create(request):
    """ Allow users to create a new recipe """
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect('recipe_list')  # Redirect to viewing page
    else:
        form = RecipeForm()
    return render(request, 'create.html', {'form': form})

@login_required
def recipe_edit(request, pk):
    """ Allow users to edit their recipes """
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)  # Ensure only owner can edit
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'edit.html', {'form': form})

@login_required
def recipe_delete(request, pk):
    """ Allow users to delete their recipes """
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')
    return render(request, 'delete.html', {'recipe': recipe})
