from rest_framework import serializers, permissions
from Inventory.models import Boxes, Constraints
from django.contrib.sites.models import Site
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    boxes = serializers.PrimaryKeyRelatedField(many=True,queryset=Boxes.objects.all())
    class Meta:
        model = User
        fields = ['id','username','boxes']
        

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boxes
        fields = ['length', 'width', 'height', 'area', 'volume','created_by','last_updated']
        read_only_fields = ['area', 'volume','created_by','last_updated']
    
    def create(self,validated_data):
        data = Site.objects.get_current().Constraints_set.all()[0]
        validated_data = area_volume(validated_data)
        temp_A1 = data.A1 - validated_data['area']
        if temp_A1 < 0:
            raise ValueError('Area is greater than allowed')
        temp_V1 = data.V1 - validated_data['volume']
        if temp_V1 < 0:
            raise ValueError('Volume is greater than allowed')
        data.A1 = temp_A1
        data.V1 = temp_V1
        data.save()
        validated_data['created_by'] = self.context['request'].user
        return Boxes.objects.create(**validated_data)
    
    def update(self,validated_data):
        data = Site.objects.get_current().Constraints_set.all()[0]
        validated_data['last_updated'] = self.context['request'].user
        c_A = validated_data['area']
        c_V = validated_data['volume']
        validated_data = area_volume(validated_data)
        c_A = data.A1 - validated_data['area'] - c_A
        if c_A < 0 :
            raise ValueError('Area is greater than allowed')
        c_V = data.V1 - validated_data['volume'] - c_V
        if c_V < 0:
            raise ValueError('Volume is greater than allowed')
        data.A1 = c_A
        data.V1 = c_V
        return Boxes.objects.update(**validated_data)
    

def area_volume(validated_data):
    validated_data['area'] = 2*(validated_data['length'] * validated_data['width'] + validated_data['length'] * validated_data['height'] + validated_data['width'] * validated_data['height'])
    validated_data['volume'] = validated_data['height'] * validated_data['area'] * validated_data['width']
    return validated_data
