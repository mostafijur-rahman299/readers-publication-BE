from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from core.models import GeneralData

def get_general_data(request):
    try:
        general_data = GeneralData.objects.first()
        if not general_data:
            return None
        return {
            "contact_email": general_data.email,
            "contact_phone": general_data.phone,
            "address": general_data.address,
            "social_links": {
                "facebook": general_data.facebook,
                "twitter": general_data.twitter,
                "instagram": general_data.instagram,
                "linkedin": general_data.linkedin
            }
        }
    except GeneralData.DoesNotExist:
        return None