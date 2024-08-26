from django.contrib import admin
from api.models import VerificationV
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class VerificationVResource(resources.ModelResource):
    class Meta:
        model = VerificationV


@admin.register(VerificationV)
class VerificationVAdmin(ImportExportModelAdmin):
    resource_classes = [VerificationVResource]
