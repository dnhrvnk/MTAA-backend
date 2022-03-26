from rest_framework import serializers

class bookSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    cover = serializers.ImageField()

class clubSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=200)
    number_of_members = serializers.IntegerField()
    photoPath = serializers.ImageField(use_url=True)

class userSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    displayName = serializers.CharField()
    photoPath = serializers.ImageField(use_url=True)
    wishlist = serializers.IntegerField()
    currently_reading = serializers.IntegerField()
    completed = serializers.IntegerField()
    recommended_books = serializers.ListField(
        child = bookSerializer()
    )
    clubs = serializers.ListField(
        child = clubSerializer()
    )

class librarySerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    cover_path = serializers.ImageField()