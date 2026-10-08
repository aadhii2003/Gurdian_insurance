from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Bypass CSRF for specific views

@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def get_csrf(request):
    return Response({'message': 'CSRF cookie set'})

@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Logged in successfully'})
    return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'full_name': f"{user.first_name} {user.last_name}".strip() or user.username
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_stats(request):
    return Response({
        'applicants': 0,
        'applications': 0,
        'policies': 0,
        'drivers': 0,
        'trucks': 0,
        'net_balance': 0,
        'transactions': 0
    })
