from django import forms
from .models import Post


# class UserForm(forms.Form):
#     username = forms.CharField(label="用户名", max_length=128)
#     password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)




class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # sex = forms.ChoiceField(label='性别', choices=gender)




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'upload', 'author')

    # overriding default form setting and adding bootstrap class
    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     self.fields['title'].widget.attrs = {'placeholder': 'Enter name', 'class': 'form-control'}
    #     self.fields['author'].widget.attrs = {'placeholder': 'Enter name', 'class': 'form-control'}
    #     self.fields['slug'].widget.attrs = {'placeholder': 'Enter email', 'class': 'form-control'}
    #     self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class': 'form-control', 'rows': '5'}
    #     self.fields['upload'].widget.attrs = {'class': 'form-control'}
