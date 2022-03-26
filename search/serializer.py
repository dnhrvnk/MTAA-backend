from rest_framework import serializers

class authorSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()

class genreSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()

class bookSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    author = serializers.ListField(
        child = authorSerializer()
    )
    genre = genreSerializer()
    pages = serializers.IntegerField()
    description = serializers.CharField()
    cover = serializers.ImageField()
    number_of_readers = serializers.IntegerField()
    rating = serializers.FloatField()

class bookFindSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    cover = serializers.ImageField()