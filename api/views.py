from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegistrationSerializer, JobsSerializer
from rest_framework.authtoken.models import Token
from ..models import Job
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework import status
import pickle
from rest_framework import serializers

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data['response'] = 'successfully registered new user.'
        data['email'] = user.email
        data['username'] = user.username
        token = Token.objects.get(user=user).key
        data['token'] = token
        return Response(data, status=status.HTTP_201_CREATED)
    error = serializer.errors.get('email',0)
    if(error[0] == 'user with this email already exists.'):
        return Response({'message':'Konto o podanym e-mailu już istnieje'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def login_view(request):
    context = {}

    email = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(email=email, password=password)
    statusResponse = ''
    if user:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        context['response'] = 'Successfully authenticated.'
        context['pk'] = user.pk
        context['email'] = email.lower()
        context['token'] = token.key
        statusResponse = status.HTTP_200_OK
    else:
        context['response'] = 'Error'
        context['message'] = 'Niepoprawny e-mail lub hasło'
        statusResponse = status.HTTP_401_UNAUTHORIZED
    return Response(context, status=statusResponse)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def getListJobs(request):
    if request.method == 'GET':
        fieldsQuery = ['id','price','title', 'dateEnd', 'jobType']
        jobs = Job.objects.all()
        serializer = JobsSerializer(jobs, many=True, fields=fieldsQuery)
        print(serializer.data)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        current_user = request.user
        _mutable = data._mutable

        # set to mutable
        data._mutable = True

        # сhange the values you want
        data['author'] = current_user.email
        data['user'] = current_user.pk
        # set mutable flag back
        data._mutable = _mutable

        serializer = JobsSerializer(data = data)


        if serializer.is_valid():
            serializer.save()
            return Response(data,status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def getJobDetails(request,pk):
    try:
        job = Job.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serilizer = JobsSerializer(job)
        return Response(serilizer.data)

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def getMyJobs(request):
    try:
        fieldsQuery = ['id', 'price', 'title', 'dateEnd', 'jobType']
        jobs = Job.objects.filter(user=request.user)
        serializer = JobsSerializer(jobs, many=True, fields=fieldsQuery)
        if request.method == 'GET':
            return Response(serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

