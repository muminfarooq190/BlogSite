from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post,Comment
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse_lazy
from blog.forms import PostForm,CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,
                                  CreateView,UpdateView,
                                  DeleteView,DetailView)


class AboutView(TemplateView):
    template_name='about.html'
    
class PostListView(ListView):
    model=Post   
    
    
    '''
    HOW TO GRAB THIS LIST? THIS METHOD WILL
    ALLOW US TO USE DJANGO's ORM
    THIS IS THE PYTHON VERSION OF WRITING SQL
    THIS MEANS GRAB THE DATES OF THAT ARE LESS OR EQUAL THEN TIMe
    AND ORDER THEM BY DESCENDING THAT MEANS MOST RECENT POST COMES ON TOp
    ''' 
    def get_queryset(self):
        return Post.objects.filter(publish_date__lte=timezone.now()). order_by('-publish_date')
     
 
 
class PostDetailView(DetailView):
    model=Post
    
class CreatePostView(CreateView,LoginRequiredMixin):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html'
    form_class=PostForm
    model=Post
        
class UpdatePostView(UpdateView,LoginRequiredMixin):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html'
    form_class=PostForm
    model=Post        

class PostDeleteView(DeleteView,LoginRequiredMixin):
    model=Post
    success_url=reverse_lazy('post_list')    
    
class PostDraftView(ListView,LoginRequiredMixin):
    login_url='/login/'
    redirect_field_name='blog/post_list.html'
    model=Post   
    '''
    THIS MEANS GET ALL THE POSTS WHICH HAVE NO PUBLICATION DATE
    COZ THOSE POSTS ARE NOT YET PUBLISHED THEY HAVE BEEN SAVED AS DRAFTS
    '''
    def get_queryset(self):
        return Post.objects.filter(publish_date__isnull=True).order_by('create_date')
    

@login_required
def add_comment_to_post(request,pk):
    '''
    HERE WE ARE GRABBING THE OBJECT OF POST
    BECAUSE COMMENT IS TO BE PUT ON POST
    
    '''
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form=CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})        

@login_required
def comment_approve(request,pk):
    '''
    HERE WE ARE GRABBING THE 
    OBJECT OF COMMENT TO APPROVE THIS COMMENT
    '''
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    '''
    comment.post.pk means ok whats the primary key
     of post this comment is linked to
    '''
    return redirect('post_detail',pk=comment.post.pk)
            

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    '''
    here we saved the pk before deleting it
    '''
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)        

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)
    