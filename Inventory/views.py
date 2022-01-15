from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from Inventory.models import Boxes
from Inventory.serializers import BoxSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
import traceback
from rest_framework import permissions
from datetime import datetime

Accepted_filters = {
    'length':'length',
    'breadth':'width',
    'height':'height',
    'area':'area',
    'volume':'volume',
    'date':'date_field',
}
Values = {
    'less':'lt',
    'more':'gt',
    'greater':'gt',
    'before':'lt',
    'after':'gt'
}

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_boxes(request,uname=None):
    try:
        final_query = {}
        try:
            queries = dict(request.GET.items())
            for query,value in queries.items():
                query = query.split('_')
                if query[0] in Accepted_filters:
                    if query[0]=='date':
                        final_query[Accepted_filters[query[0]] + '__lt'] = datetime.strptime(value,'%Y-%m-%d')
                    else:
                        final_query[Accepted_filters[query[0]] + '__' + Values[query[1]]] = value            
            username = None
            if uname is None:
                username = queries.get('username')
            elif uname== 'me':
                username = request.user.username
            if username is not None:
                final_query['created_by__username'] = username
        except:
            traceback.print_exc()
            
        print(final_query)
        boxes = Boxes.objects.filter(**final_query)
        serializer = BoxSerializer(boxes,many=True)
        if not request.user.is_staff:        
            for i in serializer.data:
                i.pop('created_by')
                i.pop('last_updated')
        return Response({"success":True,
                         "msg":"Successfully retrieved %d results"%len(serializer.data),
                         "data":serializer.data})
    except ValueError as e:
        traceback.print_exc()
        return Response({"success":False,"msg":e},status=status.HTTP_406_NOT_ACCEPTABLE)
    except:
        traceback.print_exc()
        return Response({"success":False,"msg":"Error occured"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_box(request):
    try:
        data = JSONParser().parse(request)
        serializer = BoxSerializer(data=data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response({
                'status':'success',
                'msg':'added successfully'},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        traceback.print_exc()
        return Response({"success":False,"msg":e},status=status.HTTP_406_NOT_ACCEPTABLE)
    except:
        traceback.print_exc()
        return Response({"success":False,"msg":"Error occured"}, status=status.HTTP_400_BAD_REQUEST)