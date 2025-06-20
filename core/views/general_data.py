from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import GeneralData

@api_view(['GET'])
def get_general_data(request):
    try:
        general_data = GeneralData.objects.first()
        if not general_data:
            return Response({"error": "General data not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "contact_email": general_data.email,
            "contact_phone": general_data.phone,
            "address": general_data.address,
            "address_bn": general_data.address_bn,
            "social_links": {
                "facebook": general_data.facebook,
                "twitter": general_data.twitter,
                "instagram": general_data.instagram,
                "linkedin": general_data.linkedin,
                "youtube": general_data.youtube
            },
            "articles_section": {
                "title": general_data.articles_section_title,
                "title_bn": general_data.articles_section_title_bn,
                "subtitle": general_data.articles_section_subtitle,
                "subtitle_bn": general_data.articles_section_subtitle_bn
            }
        }, status=status.HTTP_200_OK)
    except GeneralData.DoesNotExist:
        return Response({"error": "General data not found"}, status=status.HTTP_404_NOT_FOUND)