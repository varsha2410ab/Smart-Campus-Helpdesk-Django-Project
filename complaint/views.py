#api_view tells that function will take put and get methods
# permission_classes is basically JWT which protect function and only authorized person can access it 
from rest_framework.decorators import api_view,permission_classes
#to give response to frontend
from rest_framework.response import Response
#for pagination
from rest_framework.pagination import PageNumberPagination
#to import models.py
from .models import Tickets
#it fetch the details 
from rest_framework.permissions import IsAuthenticated
#to import serializers.py
from .serializers import TicketSerializer
#decorator for api
from django.views.decorators.cache import cache_page

from django.utils.decorators import method_decorator

@api_view(['GET','POST'])
#for jwt authentication
@permission_classes([IsAuthenticated])

def ticket_list(request):
    if request.method == 'GET':
        #fetch all the data from database
        tickets=Tickets.objects.all()
        #sorting
        ordering=request.query_params.get('ordering')
        #filtering
        title=request.query_params.get('title')
        #filtering
        description=request.query_params.get('description')
        #filtering
        category=request.query_params.get('category')
        #filtering
        priority=request.query_params.get('priority')
        #filtering
        
        if ordering:
            tickets=tickets.order_by(ordering)
        if title:
            tickets=tickets.filter(title__icontains=title)
        if description:
            tickets=tickets.filter(description__icontains=description)
        if category:
            tickets=tickets.filter(category__icontains=category)
        if priority:
            tickets=tickets.filter(priority__icontains=priority)
        
        #first we are calling inbuilt function then we are deciding the number of page
        #then we apply pagination to the data 
        paginator=PageNumberPagination()
        paginator.page_size=4
        paginated_tickets=paginator.paginate_queryset(tickets,request)
        #this convert data into json because frontend need json always
        serializer=TicketSerializer(paginated_tickets,many=True)
        return paginator.get_paginated_response(serializer.data)
    
    if request.method == 'POST':
        serializer=TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data,status=201)
    return Response(serializer.errors,status=400)
@cache_page(60)
@api_view(['GET','PUT','DELETE','PATCH'])
@permission_classes([IsAuthenticated])
def ticket_detail(request,id):
    try:
        tickets=Tickets.objects.get(id=id)
    except Tickets.DoesNotExist:
        return Response({'error':'Not found'},status=404)
    if request.method =='GET':
        serializer=TicketSerializer(tickets)
        return Response(serializer.data)
    if request.method =='PUT':
        serializer=TicketSerializer(tickets,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    return Response(serializer.errors,status=400)

    if request.method =='PATCH':
        serializer=TicketSerializer(tickets,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)

    if request.method =='DELETE':
        tickets.delete()
        return Response({'message':'deleted successfully'},status=204)