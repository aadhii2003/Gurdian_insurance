from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, UserSession
from .utils import generate_tokens, decode_token
from apps.common.responses import success_response, error_response
import datetime
from django.utils import timezone

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return error_response(message="Username and password are required.", status_code=400)

        try:
            user = User.objects.get(username=username, is_active=True)
            if user.check_password(password):
                access, refresh = generate_tokens(user)
                
                UserSession.objects.create(
                    user=user,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
                return success_response(data={
                    "access": access,
                    "refresh": refresh,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "full_name": user.full_name,
                        "email": user.email
                    }
                })
        except User.DoesNotExist:
            pass

        return error_response(message="Invalid credentials", status_code=401)

class RefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return error_response(message="Refresh token is required.", status_code=400)

        payload = decode_token(refresh_token)
        if not payload or payload.get('type') != 'refresh':
            return error_response(message="Invalid or expired refresh token.", status_code=401)

        try:
            user = User.objects.get(id=payload['user_id'], is_active=True)
            access, new_refresh = generate_tokens(user)
            return success_response(data={
                "access": access,
                "refresh": new_refresh
            })
        except User.DoesNotExist:
            return error_response(message="User not found or inactive.", status_code=401)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            session = UserSession.objects.filter(user=request.user, logout_time__isnull=True).order_by('-login_time').first()
            if session:
                session.logout_time = timezone.now()
                session.save()
        except Exception:
            pass
            
        return success_response(message="Logged out successfully.")

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return success_response(data={
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email
        })

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        if not current_password or not new_password:
            return error_response(message="current_password and new_password are required.", status_code=400)
            
        user = request.user
        
        if not user.check_password(current_password):
            return error_response(message="Current password is incorrect.", status_code=400)
            
        user.set_password(new_password)
        user.save()
        
        # Optionally, log out all other existing sessions for security
        UserSession.objects.filter(user=user, logout_time__isnull=True).exclude(
            ip_address=get_client_ip(request), 
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        ).update(logout_time=timezone.now())
        
        return success_response(message="Password has been changed successfully.")
