from xml.dom import ValidationErr
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

#  Custom User Manager
class UserManager(BaseUserManager):

    def create_user(self, email, first_name,username, last_name, password=None, password2=None):
        """
        Creates and saves a User with the given email, first_name, last_name and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, first_name, last_name and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_superuser

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser
   
# class MyModel(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.IntegerField()
#     email = models.EmailField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
    

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Employee(models.Model):
    emp_number = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    store_location = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    age = models.IntegerField()
    lengthservice = models.IntegerField()
    absenthours = models.DecimalField(max_digits=5, decimal_places=2)
    business_unit = models.CharField(max_length=100)
    
    def __str__(self):
        return self.emp_number

class Blog(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=100,)
    blog_image = models.ImageField(upload_to='images/',null=True,blank=True)
    blog_content = models.TextField(null=True,blank=True)
    publish_choices = (
        ('Yes', 'Published'),
        ('No', 'Draft')
    )
    is_published = models.CharField(choices=publish_choices, max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    # def custom_validator(value):
    #     valid_formats = ['png', 'jpeg']
    #     if not any([True if value.name.endswith(i) else False for i in valid_formats]):
    #         raise ValidationErr(f'{value.name} is not a valid image format')
