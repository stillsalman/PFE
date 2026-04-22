from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status

@api_view(['GET','POST',])
def get_post_training_needs(request):
    if request.method=='GET':
        needs = TrainingNeed.objects.all()
        serializer = TrainingNeedSerializer(needs, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer= TrainingNeedSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=400)
    
@api_view(['GET','DELETE','PATCH'])
def update_training_need(request,pk):
    try:
        need=TrainingNeed.objects.get(pk=pk)
    except TrainingNeed.DoesNotExist:
       return Response({"meesage": "training need not found"}, status=400)
    if request.method=="PATCH":
        serializer= TrainingNeedSerializer(need, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    elif request.method=="DELETE":
        need.delete()
        return Response({"message": "user deleted!"})
    elif request.method=="GET":
        serializer=TrainingNeedSerializer(need)
        return Response(serializer.data,status=200)
        
@api_view(['GET'])
def get_trainings(request):
    trainings=Training.objects.all()
    serializer=TrainingSerializer(trainings,many=True)
    return Response(serializer.data,status=200)
@api_view(['GET','POST','DELETE'])
def training_response(request,pk):
    try:
        training=Training.objects.get(pk=pk)
    except Training.DoesNotExist:
        return Response({"message": "training does not exist!"},status=400)
    if request.method=='GET':
        serializer=TrainingSerializer(training)
        return Response(serializer.data,status=200)
    elif request.method=='PATCH':
        serializer=TrainingSerializer(training,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)
    elif request.type=='DELETE':
        training.delete()
        return Response({"message": "training deleted!"},status=200)
    
@api_view(['POST'])
def make_decesion(request,pk):
    try:
        need=TrainingNeed.objects.get(pk=pk)
    except TrainingNeed.DoesNotExist:
        return Response({"message": "training need does not exist!"},status=400)
    serializer=DecisionSerializers(data=request.data,partial=True)
    if serializer.is_valid():
        decesion=serializer.save(TrainingNeed_id=need)
        need.status=decesion.result
        need.save()
        if decesion.result=='APPROVED':
            training=Training.objects.create(
                title=need.title,
                TrainingNeed_id=need,
                status='notassigned',
                type=request.data.get('type')
                )
        return Response({"message:" "decesion add status changed?"},status=200)
        
    return Response(serializer.errors,status=400)