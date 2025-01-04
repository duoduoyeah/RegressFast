from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic, View
from django.urls import reverse
from .models import Project
from .forms import StageOneProjectForm, StageTwoProjectForm
import pandas as pd

# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
    model = Project
    template_name = 'regression_project/index.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


# class ProjectView(LoginRequiredMixin, generic.CreateView):
#     model = Project
#     form_class = ProjectForm
#     template_name = "regression_project/create_new_project.html"
#     success_url = '/'

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

def create_new_project(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            regression_type = request.POST.get('regression_type')
            y_variable = request.POST.get('y_variable')

            # Split comma-separated variables into lists
            x_variables_str = request.POST.get('x_variables')
            x_variables = [var.strip() for var in x_variables_str.split(',')] if x_variables_str else []

            control_variables_str = request.POST.get('control_variables')
            control_variables = [var.strip() for var in control_variables_str.split(',')] if control_variables_str else []

            heterogeneous_variables_str = request.POST.get('heterogeneous_variables')
            heterogeneous_variables = [var.strip() for var in heterogeneous_variables_str.split(',')] if heterogeneous_variables_str else []

            mediating_variables_str = request.POST.get('mediating_variables')
            mediating_variables = [var.strip() for var in mediating_variables_str.split(',')] if mediating_variables_str else []

            csv_file = request.FILES.get('csv_file')

            # Create and save the Project
            project = Project.objects.create(
                name=name,
                description=description,
                csv_file=csv_file,
                regression_type=regression_type,
                y_variable=y_variable,
                x_variables=x_variables,
                control_variables=control_variables,
                heterogeneous_variables=heterogeneous_variables,
                mediating_variables=mediating_variables
            )
            project.save()

            # Redirect to the home page or wherever you'd like
            return redirect(reverse('home'))

        except Exception as e:
            # Log/handle the error and re-render form with an error message
            print(f"Error creating project: {str(e)}")
            return render(request, 'regression_project/create_new_project.html', {'error': str(e)})

    # GET request or if POST fails
    return render(request, 'regression_project/create_new_project.html')


class ProjectStageOneView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = StageOneProjectForm
    template_name = 'regression_project/create_project_stage1.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        project = form.save()
        return redirect('regression_project:create_project_stage_two', project_id=project.id)

class ProjectStageTwoView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = StageTwoProjectForm
    template_name = 'regression_project/create_project_stage2.html'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        project = get_object_or_404(Project, id=self.kwargs['project_id'], user=self.request.user)
        
        # Read CSV's first row (header) to get column names
        csv_path = project.csv_file.path
        df = pd.read_csv(csv_path, nrows=0)
        column_names = list(df.columns)
        
        # Dynamically set choices for the fields
        form.fields['x_variables'].choices = [(col, col) for col in column_names]
        form.fields['control_variables'].choices = [(col, col) for col in column_names]
        return form
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, id=self.kwargs['project_id'], user=self.request.user)
        context['project'] = project
        return context
        
    def form_valid(self, form):
        project = get_object_or_404(Project, id=self.kwargs['project_id'], user=self.request.user)
        project.x_variables = form.cleaned_data['x_variables']
        project.control_variables = form.cleaned_data['control_variables']
        project.save()
        return redirect('regression_project:index')