import json
from django.shortcuts import render
import logging
from rest_framework.generics import GenericAPIView
from app.models import Employee, Task, User
from app.serializers import TaskSerializer, UserSerializer,EmployeeSerializer,CustomTokenObtainPairSerializer
import datetime
from django.shortcuts import render
import logging
from rest_framework.generics import GenericAPIView
from app.models import Blog, User
from app.serializers import BlogSerializer, UserSerializer,CustomTokenObtainPairSerializer, verifyAccountSerializer
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.response import Response
from django.utils.encoding import force_bytes
from rest_framework import status, serializers, generics
from app.renderers import UserRenderer
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from .utils import send_otp_via_mail
from rest_framework.permissions import IsAuthenticated

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
                send_otp_via_mail(serializer.data['email'])
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

        if user and user.is_verified is False:
            return Response({'errors': {'non_field_errors': ['Please Verify your Email to login']}},
                            status=status.HTTP_404_NOT_FOUND)

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
    
    def put(self, request, format=None):
        file_obj = request.FILES['file']
        df = pd.read_csv(file_obj)
        data = df.to_dict('records')
        for item in data:
            emp_number = item['emp_number']
            employee = Employee.objects.filter(emp_number=emp_number).first()
            if employee:
                serializer = self.get_serializer(employee, data=item, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return Response({'msg': 'Successfully Updated'}) 
class EmployeeFilterView(generics.ListAPIView):
    queryset = Employee.objects.select_related('job_title')
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        job_title = self.request.query_params.get('job_title')
        city = self.request.query_params.get('city')
        # queryset =  Employee.objects.filter(job_title= job_title,city=city).order_by('user_name').all()
        if job_title and city:
            queryset = Employee.objects.filter(
                Q(job_title__icontains=job_title) and Q(city__icontains=city)
            )
        elif job_title:
            queryset = Employee.objects.filter(job_title__icontains=job_title)
        elif city:
            queryset = Employee.objects.filter(city__icontains=city)
        else:
            queryset = Employee.objects.all()
        return queryset
class VerifyOTP(GenericAPIView):
    def post(self, request):
        try:
            data = request.data
            serializer = verifyAccountSerializer(data = data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
            import pdb ; pdb.set_trace()
            user = User.objects.get(email=email)
            if not user:
                return Response({
                        'status' : 400,
                        'message' : 'Failed',
                        'data' : 'Invalid Email',
                    }) 

            if not otp == otp:
                return Response({
                        'status' : 400,
                        'message' : 'Failed',
                        'data' : 'Wrong OTP',
                    }) 
            user.is_verified = True
            user.save()

            return Response({
                'status' : 200,
                'message' : 'Verification Successful',
                'data' : serializer.data,
            }) 
        except Exception as e:
            return Response({
                    'status' : 400,
                    'message' : 'Failed',
                    'data' : serializer.errors,
                })  

class BlogView(GenericAPIView):
    renderer_classes = (UserRenderer,)
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer

    def post(self, request, format=None):
        '''
        This method is used to register the user.
        '''
        try:
            user = request.user
            data = request.data
            user_blogs =Blog.objects.filter(user=self.request.user).values_list('blog_title',flat=True)
            blog_title = request.data.get('blog_title')
            is_published = request.data.get('is_published')
            if blog_title:
                if blog_title in user_blogs:
                    return Response({'msg': 'Blog name already exist'}, status=status.HTTP_403_FORBIDDEN)
                # if is_published == 'Yes':
                #     data['published_at'] = datetime.datetime.now()
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=user)
                return Response({'msg': 'Blog created'},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Blog title required'},
                                status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, formate= None):
        try:
            blogs= Blog.objects.filter(user = request.user)
            serializer = self.serializer_class(blogs, many=True)
            return Response(serializer.data,
                            status=status.HTTP_200_OK) 
        except Exception as e:
            logger.error(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request,blog_id, format=None):
        '''
        This method is used to register the user.
        '''
        try:
            # import pdb; pdb.set_trace()
            user = request.user
            user_blogs =Blog.objects.get(id=blog_id)
            serializer = BlogSerializer(user_blogs, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response({'msg': 'Blog Updated'},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request,blog_id, format=None):
        if Blog.objects.filter(id=blog_id).exists():
            Blog.objects.get(id=blog_id).delete()
        else:
            raise serializers.ValidationError(
                "The Blog does not exist, Kindly make a POST request to create the Blog")

        return Response({"Result": "Blog Deleted"}, status=status.HTTP_204_NO_CONTENT)

class PublishedBlogs(GenericAPIView):
    renderer_classes = (UserRenderer,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer

    def get(self, request, format=None):
        blogs = Blog.objects.filter(is_published='Yes')
        serializer = self.serializer_class(blogs, many=True, context={'user': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)
