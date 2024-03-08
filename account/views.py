from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView,TemplateView
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import RegistrationForm
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin








class CustomRegistrationView(UserPassesTestMixin,CreateView):
    model = CustomUser
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
                    if form.cleaned_data['password1'] != form.cleaned_data['password2']:
              
                        messages.error(self.request, 'Passwords do not match.')
                        return self.render_to_response(self.get_context_data(form=form))

                    response = super().form_valid(form)

                    messages.success(self.request, 'Registration successful. You can now log in.')
                    return redirect(self.get_success_url())

                
                    
    def get_success_url(self):
        
        return self.success_url
    
    def test_func(self):
        return not self.request.user.is_authenticated
    
    
    

    def form_invalid(self, form):
       
        if 'email' in form.errors:
            messages.error(self.request, f"Invalid email: {form['email'].value()}")
        if 'password1' in form.errors:
            messages.error(self.request, 'Invalid password. Passwords must match and meet the criteria.')
        
        if 'name' in form.errors:
            messages.error(self.request, 'Invalid name. Please provide a valid name.')

        if 'country' in form.errors:
            messages.error(self.request, 'Invalid country. Please provide a valid country.')

        

        return self.render_to_response(self.get_context_data(form=form))
    
class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.redirect_authenticated_user()

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return self.redirect_authenticated_user()

        return super().get(request, *args, **kwargs)

    def redirect_authenticated_user(self):
        user = self.request.user
        role = getattr(user, 'role', None)

        if role in ['student', 'staff', 'admin', 'editor']:
            return redirect(f'{role}_dashboard')
        else:
            messages.error(self.request, 'Invalid user role.')

        return redirect('default_dashboard')

    def get_success_url(self):
        user = self.request.user
        role = getattr(user, 'role', None)

        if user.is_authenticated and role in ['student', 'staff', 'admin', 'editor']:
            return reverse(f'{role}_dashboard')

        messages.error(self.request, 'Invalid user role.')
        return reverse('default_dashboard')





class StudentDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'student_dashboard.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'student'

class StaffDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'staff_dashboard.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'staff'

class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

class EditorDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'editor_dashboard.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'editor'



def index(request):
   return render(request,'index.html')


@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return redirect('index')