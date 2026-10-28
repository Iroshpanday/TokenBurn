from django.db import models

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Project (models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AIRequest(models.Model):
    STATUS_CHOICES = [
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    prompt = models.TextField()
    response = models.TextField(null=True, blank=True)
    model_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    error_message = models.TextField(null=True, blank=True)
    input_tokens = models.IntegerField(default=0)
    output_tokens = models.IntegerField(default=0)
    cost = models.FloatField(default=0)
    latency_ms = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} - {self.status}"
