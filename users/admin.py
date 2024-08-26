from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.formats import base_formats

from users.models import User


# Register your models here.


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'email', 'is_staff', 'is_active')

    # def get_export_formats(self):
    #     formats = (
    #         base_formats.CSV,
    #         base_formats.XLSX,
    #         base_formats.JSON,
    #         base_formats.HTML,
    #         base_formats.ODS
    #     )
    #
    #     return [f for f in formats if f().can_export()]

