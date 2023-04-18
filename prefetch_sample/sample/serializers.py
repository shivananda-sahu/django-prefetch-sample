from rest_framework import serializers
from .models import Person, Group


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'


class FilteredPersonListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(membership__is_active=True)
        return super(FilteredPersonListSerializer, self).to_representation(data)


class FilteredPersonSerializer(PersonSerializer):

    class Meta:
        list_serializer_class = FilteredPersonListSerializer
        model = Person
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    members = FilteredPersonSerializer(many=True)

    class Meta:
        model = Group
        fields = '__all__'
