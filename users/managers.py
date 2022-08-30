from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, email: str, password: str, **extra_fields: dict):

        if not email:
            raise ValueError("The email field must be informed.")

        if extra_fields.get("first_name", False):
            extra_fields["first_name"] = extra_fields["first_name"].title()

        if extra_fields.get("last_name", False):
            extra_fields["last_name"] = extra_fields["last_name"].title()

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self.db)

        return user

    def _update_user(self, instance,  **update_fields: dict):

        if update_fields.get("first_name", False):
            update_fields["first_name"] = update_fields["first_name"].title()

        if update_fields.get("last_name", False):
            update_fields["last_name"] = update_fields["last_name"].title()

        if update_fields.get("email", False):
            update_fields["email"] = self.normalize_email(update_fields["email"])

        for key, value in update_fields.items():

            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

            instance.save(using=self.db)

        return instance

    def create_user(self, email: str, password: str, **extra_fields: dict):

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields: dict):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_seller", False)

        return self._create_user(email, password, **extra_fields)

    def update_user(self, instance, **update_fields: dict):

        update_fields.setdefault("is_staff", False)
        update_fields.setdefault("is_superuser", False)

        return self._update_user(instance, **update_fields)