from django import forms
from .models import Project

class StageOneProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'csv_file']  # Only these fields for the first step

class StageTwoProjectForm(forms.ModelForm):
    # In the second form, we *don't* rely entirely on the Project model fields
    # because we want to dynamically set choices based on the CSV column names
    x_variables = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Independent Variables"
    )
    control_variables = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Control Variables"
    )

