from django.db import models
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view

class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    class Meta:
        managed=False
        db_table = 'authors'

class AuthorSerialize(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


@api_view(['GET'])
def testGet(response):
    items = Author.objects.all()
    for e in items:
        print(e.name)
    return Response(AuthorSerialize(items,many=True).data)
