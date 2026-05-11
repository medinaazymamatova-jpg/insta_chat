from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, blank=True,
                                           validators=[MinValueValidator(14), MaxValueValidator(100)],)
    phone_number = PhoneNumberField()
    user_image = models.ImageField(null=True, blank=True, upload_to='image_user/')
    bio = models.TextField(null=True, blank=True)
    user_network = models.URLField(null=True, blank=True)
    certificate = models.BooleanField(default=False)
    date_register = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.username}, {self.first_name}'

    def get_count_follower(self):
        return self.follower_user.count()

    def get_count_following(self):
        return self.following_user.count()

    def get_count_post(self):
        return self.post_user.count()

class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower_user')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following_user')

class Hashtag(models.Model):
    hashtag_name = models.CharField(max_length=64)

    def __str__(self):
        return self.hashtag_name

class Post(models.Model):
    music = models.FileField(upload_to='post_music/')
    hashtag = models.ManyToManyField(Hashtag, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    people = models.ManyToManyField(UserProfile, null=True, blank=True, related_name='post_user')
    created_date = models.DateField(auto_now_add=True)

    def get_count_post_like(self):
        return self.post_like.count()

    def get_count_post_comment(self):
        return self.post_comment.count()


class Content(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_content')
    file = models.FileField(upload_to='content_file/')

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='postlike_user')
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comment_user')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comment_like_user')
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'comment')

class SavePost(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

class SavePostItem(models.Model):
    save_post = models.ForeignKey(SavePost, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Stories(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='stories_user')
    file = models.FileField(upload_to='storia_file/')
    created_date = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField(auto_now_add=True)

class Massage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='massage_image/')
    file = models.FileField(upload_to='massage_file/')
    created_date = models.DateTimeField(auto_now_add=True)
