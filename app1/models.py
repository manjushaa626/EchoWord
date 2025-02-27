from django.db import models

# Create your models here.
class Blogpost(models.Model):
    user = models.ForeignKey('auth.User',related_name='blogs', on_delete=models.CASCADE)
    title = models.CharField(max_length=200) 
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/') 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
  

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user= models.OneToOneField('auth.User',on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=12)
    profile_photo = models.ImageField(upload_to='profile_photos/', default='profile_photos/default.jpg')


class Comment(models.Model):
    blog = models.ForeignKey(Blogpost, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.user', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)