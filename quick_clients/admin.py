# Django
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Local
from quick_clients.models import Client


class ClientCreationForm(forms.ModelForm):
    """A form for creating new clients"""

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = Client
        fields = (
            'username', 'email', 'document',
            'first_name', 'last_name'
        )

    def clean_password2(self):
        """Check that the two password entries match"""

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        """Save the provided password in hashed format"""

        client = super().save(commit=False)
        client.set_password(self.cleaned_data["password1"])

        if commit:
            client.save()
        return client


class ClientChangeForm(forms.ModelForm):
    """A form for updating clients."""

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Client
        fields = (
            'username', 'email',
            'password', 'document',
            'first_name', 'last_name',
            'is_active', 'is_staff',
        )


class ClientAdmin(BaseUserAdmin):
    """The forms to add and change user instances."""

    add_form = ClientCreationForm
    form = ClientChangeForm

    fieldsets = [
        ("Nombres", {"fields": ["first_name", "last_name"]}),
        ("Documentación", {"fields": ["document"]}),
        ("Credenciales", {"fields": ["username", "email", "password"]}),
        ("Atributos", {"fields": ["is_active", "is_staff", "is_superuser"]}),
        ("Otros", {"fields": ["last_login"]})
    ]

    search_fields = ['first_name', "last_name"]
    list_display = ("__str__", "email")
    list_filter = ('is_staff',)
    ordering = ('email', 'document')
    filter_horizontal = ()


admin.site.register(Client, ClientAdmin)
admin.site.unregister(Group)
