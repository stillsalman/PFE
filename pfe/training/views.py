from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TrainingNeed
from .serializers import TrainingNeedSerializer


@api_view(['GET'])
def get_training_needs(request):
    needs = TrainingNeed.objects.all()
    serializer = TrainingNeedSerializer(needs, many=True)
    return Response(serializer.data)