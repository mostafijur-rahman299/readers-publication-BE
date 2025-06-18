from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SupportSerializer
from .models import Support, GeneralData, Carousel
from .serializers import SupportSerializer, GeneralDataSerializer, CarouselSerializer


class SupportCreateView(CreateAPIView):
    serializer_class = SupportSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GeneralDataRetrieveView(RetrieveAPIView):
    serializer_class = GeneralDataSerializer
    queryset = GeneralData.objects.all()

    def get(self, request):
        general_data = self.get_object()
        serializer = self.serializer_class(general_data)
        return Response(serializer.data)
        

class CarouselListAPIView(ListAPIView):
    serializer_class = CarouselSerializer
    queryset = Carousel.objects.all()

    def get(self, request):
        carousel = self.get_queryset()
        serializer = self.serializer_class(carousel, many=True)
        return Response(serializer.data)
    

