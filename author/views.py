from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from author.models import Author
from author.serializers import AuthorSerializer

class AuthorViewSet(viewsets.ViewSet):
    def list(self, request):
        authors = Author.objects.filter(is_active=True).order_by('name')
        serializer = AuthorSerializer(authors, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            author = Author.objects.get(pk=pk, is_active=True)
            serializer = AuthorSerializer(author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Author.DoesNotExist:
            return Response({"detail": "Author not found."}, status=status.HTTP_404_NOT_FOUND)
