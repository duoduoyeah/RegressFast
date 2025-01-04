from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout

class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = "home/home.html"
    login_url = '/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Run Regression Fast'
        context['welcome_message'] = f'Welcome, {self.request.user.username}!'
        context['description'] = ('Start a project, then upload your CSV file'
                                'below for processing.We support various CSV'
                                'formats and will help you analyze '
                                'and transform your data.')
        return context

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page.
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials.'})
    else:
        return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')



