from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from ..seraliazers import UserSerializer
from ..models import User
import jwt, datetime
from rest_framework.permissions import AllowAny
from jwt import DecodeError
from rest_framework.exceptions import AuthenticationFailed


def time_to_num(time_str):
    hh, mm , ss = map(int, time_str.split(':'))
    return ss + 60*(mm + 60*hh)
    
def datetime_to_int(dt):
    return int(dt.strftime("%Y%m%d%H%M%S"))
    
# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        # Get the current time as a datetime object
        now = datetime.datetime.now()

        # Convert the current time to an integer timestamp
        issued_at = int(now.timestamp())/100000

    
        # Calculate the expiry time 60 minutes from now
        expiry_time = issued_at + 60 * 60  # 60 minutes * 60 seconds

        payload = {
            'id':  int(user.id),
            'exp': expiry_time,
            'iat': issued_at
        }

        try:
            token = jwt.encode(payload, 'secret', algorithm='HS256')
        except jwt.PyJWTError as e:
            raise AuthenticationFailed('Failed to generate token')

        response = Response()

        try:
            response.set_cookie(key='jwt', value=token, httponly=True, samesite = None)
        except DecodeError as e:
            # Handle the exception, such as logging an error message
            print("Error setting JWT cookie:", e)
            
        response.data = {
            'jwt': token
        }
        return response
    

class UserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
