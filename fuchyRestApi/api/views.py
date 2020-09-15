from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegistrationSerializer, JobsSerializer
from rest_framework.authtoken.models import Token
from ..models import Job


@api_view(['POST', ])
def registration_view(request):

	if request.method == 'POST':
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['username'] = account.username
			token = Token.objects.get(user=account).key
			data['token']=token
		else:
			data = serializer.errors
		return Response(data)
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def getListJobs(request):
	jobs = Job.objects.all()
	serializer = JobsSerializer(jobs, many=True)
	return Response(serializer.data)
