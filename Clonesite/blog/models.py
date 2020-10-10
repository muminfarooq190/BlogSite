from django.db import models
from django.utils import timezone
from django.urls import reverse

class Post(models.Model):
    author=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title=models.CharField(max_length=28)
    text=models.CharField(max_length=264)
    create_date=models.DateTimeField(default=timezone.now)
    publish_date=models.DateTimeField(blank=True,null=True)
    
    
    '''THIS METHOD WILL SHOW THE PUBLI
        -CATION DATE OF A POST'''
    def publish(self):
        self.publish_date=timezone.now()
        self.save()
    
    '''
    THIS METHOD IS GOING TO APPROVE THE COMMENTS FROM SUPER_USER
    IN THIS CASE WE HAVE ALREADY CONNECTED SUPERUSER TO THE AUTHOR
    '''
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)    
    '''
    THIS METHOD WILL DECIDE WHERE TO REDIRECT A USER AFTER HE HAS COMPL
    ETED CREATING A POST
    '''
    def get_absolute_url(self):
        return reverse('post_detail',kwargs={'pk':self.pk})
        
    def __str__(self):
        return self.title    
    
'''
THIS MODEL HERE IS LIKE BABY OF POST
HERE FIRST FIELD IS CONNECTED TO THE POST SO COMMENTS CAN BE CONNECTED
TO A SPECIFIC POST
'''
class Comment(models.Model):
    post=models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author=models.CharField(max_length=264)
    text=models.CharField(max_length=254)
    create_date=models.DateTimeField(default=timezone.now)
    approved_comment=models.BooleanField(default=False)
    
    def approve(self):
        self.approved_comment=True
        self.save()
    
    def __str__(self):
        return self.text    
    
    '''
    AFTER COMMENTING A USER SHOULD BE REDIRECTED TO THE HOME PAGE
    IN OUR CASE HOME PAGE IS THE LIST OF BLOGS
    '''
    def get_absolute_url(self):
        return reverse('post_list') 