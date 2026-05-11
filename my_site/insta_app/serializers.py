from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'age')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    # def to_representation(self, instance):
    #     refresh = RefreshToken.for_user(instance)
    #     return {
    #         'user': {
    #             'username': instance.username,
    #             'email': instance.email,
    #         },
    #         'access': str(refresh.access_token),
    #         'refresh': str(refresh),
    #     }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileListSerializer(serializers.ModelSerializer):
    count_follower = serializers.SerializerMethodField()
    count_following = serializers.SerializerMethodField()
    count_post = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['id', 'user_image', 'first_name', 'username', 'count_post', 'count_following', 'count_follower']

    def get_count_follower(self, obj):
        return obj.get_count_follower()

    def get_count_following(self, obj):
        return obj.get_count_following()

    def get_count_post(self, obj):
        return obj.get_count_post()

class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_image', 'username']

class FollowSerializer(serializers.ModelSerializer):
    follower_user = UserProfileListSerializer(many=True, read_only=True)
    following_user = UserProfileListSerializer(many=True, read_only=True)
    class Meta:
        model = Follow
        fields = [ 'id', 'follower_user', 'following_user']


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['hashtag_name']

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['file']

class PostListSerializer(serializers.ModelSerializer):
    post_content = ContentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ['id', 'post_content']

class PostDetailSerializer(serializers.ModelSerializer):
    post_content = ContentSerializer(read_only=True, many=True)
    hashtag = HashtagSerializer(many=True)
    created_date = serializers.DateField()
    people = UserProfileListSerializer(read_only=True, many=True)
    count_post_like = serializers.SerializerMethodField()
    count_post_comment = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['post_content', 'hashtag', 'description', 'people', 'created_date', 'count_post_like', 'count_post_comment'
                  ]

    def get_count_post_like(self, obj):
        return obj.get_count_post_like()

    def get_count_post_comment(self, obj):
        return obj.get_count_post_comment()


class PostLikeSerializer(serializers.ModelSerializer):
    post = PostDetailSerializer(read_only=True)
    user = UserProfileCommentSerializer(read_only=True)
    class Meta:
        model = PostLike
        fields = ['post', 'user', 'like']


class CommentSerializer(serializers.ModelSerializer):
    post = PostDetailSerializer(read_only=True)
    user = UserProfileCommentSerializer(read_only=True)
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    class Meta:
        model = Comment
        fields = ['post', 'user', 'text', 'created_date']

class CommentLikeSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only=True)
    user = UserProfileCommentSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ['comment', 'user', 'like']


class SavePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavePost
        fields = '__all__'

class SavePostItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavePostItem
        fields = '__all__'

class StoriesSerializer(serializers.ModelSerializer):
    user = UserProfileCommentSerializer(read_only=True)
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    class Meta:
        model = Stories
        fields = ['user', 'file', 'created_date']