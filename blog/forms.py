from django import forms
from .models import Post, Category, Comment

class PostForm(forms.ModelForm):
    # Define the categories field with a ModelChoiceField and Tailwind styling
    categories = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a Category",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories', 'image']  # Only the 4 fields: title, content, categories, image

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        # Apply Tailwind classes for the title field
        self.fields['title'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-blue-500',
            'placeholder': 'Enter title'
        })
        
        # Apply Tailwind classes for the content field
        self.fields['content'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-blue-500',
            'rows': 10,
            'placeholder': 'Write your content here'
        })
        
        # Apply Tailwind classes for the image field
        self.fields['image'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
        })


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Only the 1 field: content
        widgets = {
            'content':forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }