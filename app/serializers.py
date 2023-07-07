from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from app.models import Employee, Task, User
import re, logging

logger = logging.getLogger('django')

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password',]

    def create_user_from_link(context):
        token = context.get('payload')
        email = token.get('email')
        role = token.get('role')
        if token.get('first_name') and token.get('last_name'):
            first_name = token.get('first_name')
            last_name = token.get('last_name')
            user = User.objects.create(email=email, first_name=first_name, last_name=last_name, type_of_account=role,
                                       is_invited="True")
        else:
            user = User.objects.create(email=email, type_of_account=role, is_invited="True")
        return user

    def create(self, validate_data):
        if validate_data.get('email'):
            validate_data['email']=validate_data.get('email').lower()
        return User.objects.create_user(**validate_data)

    def validate(self, attrs):
        min_length=8
        max_length=25
        
        password = attrs.get('password')
        
        if len(password) < min_length or len(password) > max_length:
            raise serializers.ValidationError("Password length must be 8-25 characters")
        if not re.findall('[A-Z]', password):
            raise serializers.ValidationError(
                ("The password must contain at least one uppercase letter, A-Z."),
                code='password_no_upper',
            )
        if not re.findall('[a-z]', password):
            raise serializers.ValidationError(
                ("The password must contain at least one lowercase letter, a-z."),
                code='password_no_lower',
            )
        if not re.findall('[0-9]', password):
            raise serializers.ValidationError(
                ("The password must contain at least one number, 0-9."),
                code='password_no_num',
            )
        if not re.findall('[^\w\*]', password):
            raise serializers.ValidationError(
                ('The password must contain at least one special character, /[*@!#%&()^~}{]+/'),
                code='password_no_symbol',
            )
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser
        user.refresh_token = str(token)
        user.save()
        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title','description','due_date','completed']
        

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        