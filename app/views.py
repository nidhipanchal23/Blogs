import json
from django.shortcuts import render
import logging
from rest_framework.generics import GenericAPIView
from app.models import Employee, Task, User
from app.serializers import TaskSerializer, UserSerializer,EmployeeSerializer,CustomTokenObtainPairSerializer
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.response import Response
from django.utils.encoding import force_bytes
from rest_framework import status, serializers, generics
from app.renderers import UserRenderer
from django.contrib.auth import authenticate


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd

logger = logging.getLogger('django')
# Create your views here.
class UserRegistrationView(GenericAPIView):
    renderer_classes = [UserRenderer]

    serializer_class = UserSerializer

    def post(self, request, format=None):
        '''
        This method is used to register the user.
        '''
        try:
            email = request.data.get('email').lower()
            if email in User.objects.values_list('email', flat=True):
                return Response({'msg': 'An account with the given email already exists'}, status=status.HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.id))
                # verify_email(request, user, uid)
            return Response({'uid': uid, 'email': email,
                             'msg': 'Registration Successful, Email verification link sent. Please verify your email.'},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLoginView(GenericAPIView):
    renderer_classes = (UserRenderer,)

    def post(self, request, format=None):
        '''
        This method is used to login.
        '''
        email = request.data.get('email').lower()
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        # if user and user.is_verified is False:
        #     return Response({'errors': {'non_field_errors': ['Please Verify your Email to login']}},
        #                     status=status.HTTP_404_NOT_FOUND)
        user.is_verified= True    
        if user and user.is_active:
            token = CustomTokenObtainPairSerializer.get_token(user)
            return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}},
                            status=status.HTTP_404_NOT_FOUND)


# class TaskView(GenericAPIView):
#     renderer_classes = [UserRenderer]
#     serializer_class = TaskSerializer
class TaskCreateView(GenericAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = TaskSerializer

    def post(self, request, format = None):
        task_name = request.data.get('title')
        if task_name in Task.objects.values_list('title',flat=True):
            return Response("Task name already assigned")
        else:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)  
            serializer.save(user=self.request.user)
            serializer.save()
            return Response({'msg': 'Task Assign'}, status=status.HTTP_200_OK)
    
    def get(self, request,format=None):
        task = Task.objects.all()
        serializer = TaskSerializer(task, many=True,context={"request":request}) 

        return Response({'Task':serializer.data})


class EmployeeDataView(GenericAPIView):
    # queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def post(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()
        file_obj = request.FILES['file']
        df = pd.read_csv(file_obj)
        data=df.to_dict('records')
        for item in data:
            emp_number = item['emp_number']
            if Employee.objects.filter(emp_number=emp_number).exists():
                return Response({"error": "An Employee with this id already exists."})
        else:
            serializer = self.get_serializer(data=df.to_dict('records'), many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'msg': 'Successfully Uploaded'}, status=status.HTTP_201_CREATED)

    def get(self, request,format=None):
        task = Task.objects.all()
        serializer = EmployeeSerializer(task, many=True,context={"request":request}) 

        return Response({'Data':serializer.data})
    
    def delete(self, request):
        serializer = EmployeeSerializer()
        queryset = serializer.Meta.model.objects.all()
        queryset.delete()
        return Response({"message": "All records have been deleted."})