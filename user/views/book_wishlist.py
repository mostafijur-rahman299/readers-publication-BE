from rest_framework.views import APIView
from user.models import BookWishList
from user.serializers import UserBookWishListSerializerRead
from rest_framework.response import Response
from rest_framework import status
from book.models import Book

class UserBookWishListAPIView(APIView):
    serializer_class = UserBookWishListSerializerRead
    queryset = BookWishList.objects.all()

    def get(self, request):
        user = request.user
        wishlist = BookWishList.objects.filter(user=user)
        serializer = self.serializer_class(wishlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        book = Book.objects.get(id=book_id)
        wishlist = BookWishList.objects.create(user=user, book=book)
        serializer = self.serializer_class(wishlist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    