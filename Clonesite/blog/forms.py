from django import forms
from blog.models import Post,Comment

class PostForm(forms.ModelForm):
    
    class Meta():
        model=Post
        fields=('author','title','text')
        
        widgets={
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }
class CommentForm(forms.ModelForm):
    class Meta():
        fields=('author','text')
        model=Comment
        
        
        '''
         THESE WIDGETS WE USE TO STYLE THE FIELDS BY GIVING THEM CLASSES
         WE CAN TARGET THESE CLASSES IN CSS AND ALSO SOME OF THEM ARE PREDEFINED
         WE JUS NEED TO INSTALL LIBRARIES FOR IT:)
        '''
        
        widgets={
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea '})
        }        