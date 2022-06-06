from django.contrib.auth.models import BaseUserManager


class ClientManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("No es posible crear un usuario sin email")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields["is_staff"] is False:
            raise ValueError(
                "No es posible crear un superuser si is_staff no es True"
            )
        if extra_fields["is_superuser"] is False:
            raise ValueError(
                "No es posible crear un superuser si is_superuser no es True"
            )

        return self.create_user(email, password, **extra_fields)
