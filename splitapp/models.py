from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, mobile, password=None,password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            mobile=mobile
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile, password=None,password2=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            name=name,
            mobile=mobile,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    mobile=models.BigIntegerField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name","mobile"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
# share_type = models.CharField(max_length=50, choices=[('EQUAL', 'Equal'), ('EXACT', 'Exact'), ('PERCENT', 'Percent'), ('SHARE', 'Share')])

class Expense(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    notes=models.TextField()
    image=models.ImageField(upload_to='media')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_paid')
    participants = models.ManyToManyField(User, through='ExpenseParticipant')
    created_at = models.DateTimeField(auto_now_add=True)
    share_type = models.CharField(max_length=50, choices=[('EQUAL', 'Equal'), ('EXACT', 'Exact'), ('PERCENT', 'Percent'), ('SHARE', 'Share')],default="EQUAL")
    def __str__(self):
        return self.name

class ExpenseParticipant(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share_type = models.CharField(max_length=50, choices=[('EQUAL', 'Equal'), ('EXACT', 'Exact'), ('PERCENT', 'Percent'), ('SHARE', 'Share')],default="EQUAL")
    value = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True)
    def __str__(self):
        return f"{self.user.name} - {self.share_type}"

class Balance(models.Model):
    debtor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balances_debtor')
    creditor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balances_creditor')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
