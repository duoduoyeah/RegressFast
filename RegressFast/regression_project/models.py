from django.db import models
from django.contrib.auth.models import User  

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    REGRESSION_CHOICES = [
        ('PANEL', 'Panel Data Analysis'),
        ('DID', 'Difference in Differences'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    csv_file = models.FileField(upload_to='project_files/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Project settings
    regression_type = models.CharField(
        max_length=10,
        choices=REGRESSION_CHOICES,
        default='DID'
    )
    x_variables = models.JSONField(help_text="List of independent variables", default=list)
    y_variable = models.CharField(max_length=100, help_text="Dependent variable")
    control_variables = models.JSONField(
        blank=True, 
        null=True, 
        help_text="List of control variables", 
        default=list
    )
    heterogeneous_variables = models.JSONField(
        blank=True,
        null=True, 
        help_text="List of heterogeneous variables",
        default=list
    )
    mediating_variables = models.JSONField(
        blank=True,
        null=True,
        help_text="List of mediating variables",
        default=list
    )
    # Results
    results = models.JSONField(blank=True, null=True, help_text="Regression results")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

