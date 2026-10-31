from django.contrib import admin

from .models import AIRequest, Organization, Project


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "organization", "created_at")


@admin.register(AIRequest)
class AIRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project",
        "model_name",
        "status",
        "input_tokens",
        "output_tokens",
        "cost",
        "latency_ms",
        "created_at",
    )
    list_filter = ("status", "model_name")
