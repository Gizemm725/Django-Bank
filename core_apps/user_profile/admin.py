from django.contrib import admin
from cloudinary.forms import CloudinaryFileField  # Küçük harf değil, doğru: CloudinaryFileField
from django import forms
from django.utils.html import format_html  # 'fomat_html' yanlış yazılmış
from django.utils.translation import gettext_lazy as _

from .models import NextOfKin, Profile


class ProfileAdminForm(forms.ModelForm):
    photo = CloudinaryFileField(
        options={"crop": "fill", "width": 200, "height": 200, "folder": "bank_photos"},
        required=False,
    )

    class Meta:
        model = Profile
        fields = '__all__'


class NextOfKinInline(admin.TabularInline):
    model = NextOfKin
    extra = 1
    fields = ("first_name", "last_name", "relationship", "phone_number", "is_primary")  # {} yerine () kullandım


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = [
        'user',
        'full_name',
        'email',
        'phone_number',
        'employment_status',
        'photo_preview',
    ]
    list_display_links = ["user"]
    list_filter = ["gender", "marital_status", "employment_status", "country"]
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'phone_number']

    readonly_fields = ['user']

    fieldsets = (
        (
            _("Personal Information"),
            {"fields": ("user", "photo", "is_photo", "signature_photo", "title", "gender", "date_of_birth", "marital_status")},
        ),
        (
            _("Contact Information"),
            {"fields": ("phone_number", "address", 'city', 'country')},
        ),
        (
            _("Identification"),
            {"fields": ("means_of_identification", "id_issue_date", "id_expiry_date", "passport_number")},
        ),
        (
            _("Employment Information"),
            {"fields": ("employment_status", "employer_name", "annual_income", "date_of_employment", "job_title",
                        "department", "work_email", "work_phone_number", "employer_address", "employer_city", "employer_state")},
        ),
    )

    inlines = [NextOfKinInline]

    def full_name(self, obj) -> str:
        return obj.user.full_name

    full_name.short_description = _("Full Name")

    def email(self, obj) -> str:
        return obj.user.email

    email.short_description = _("Email")

    def photo_preview(self, obj) -> str:
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit:cover;" />',
                obj.photo.url
            )
        return "No Photo Yet"

    photo_preview.short_description = _("Photo")

@admin.register(NextOfKin)
class NextOfKinAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'relationship',
        'profile',
        'is_primary',
    ]
    list_filter = ['relationship', 'is_primary']
    search_fields = ['first_name', 'last_name', 'profile__user__email']


    def full_name(self, obj) -> str:
        return f"{obj.first_name} {obj.last_name}"

    full_name.short_description = _("Full Name")
