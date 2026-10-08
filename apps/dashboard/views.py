from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.common.responses import success_response

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return success_response(data={
            "welcome": f"Welcome back, {request.user.username}! Here's your system overview.",
            "stats": {
              "applicants": 1,
              "applications": 1,
              "policies": 0,
              "net_balance": 0,
              "transactions": 0,
              "drivers": 1,
              "trucks": 1
            },
            "recent_applicants": [
              {
                "id": 3,
                "business_name": "NOVA TERRA SOLUTIONS LLC",
                "account_name": None,
                "city": "TOPEKA",
                "status": "In Progress",
                "created_at": "2026-09-14"
              }
            ],
            "recent_applications": [
              {
                "id": 3,
                "business_name": "NOVA TERRA SOLUTIONS LLC",
                "business_line": "Package",
                "status": "submitted",
                "created_at": "2026-09-17"
              }
            ],
            "recent_transactions": []
        })
