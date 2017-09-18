# -*- coding: utf-8 -*-

from django import forms

class LoginForm(forms.Form):
    uid =forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'uid', 'placeholder':'用户名'}))
    pwd = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'pwd','placeholder':'密码'}))


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'id':'username', 'class':'form-control','placeholder':'用户名','onblur':'authentication()'}))
    # onblur 鼠标离开这个元素执行的方法
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'id':'email','placeholder':'邮箱'}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control', 'id':'avatar','placeholder':'用户头像'}))
    profile = forms.CharField(widget=forms.Textarea(attrs={'cols':'40','rows':'4','id':'profile', 'class':'form-control','placeholder':'用户简介'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'pwd1','placeholder':'密码'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'pwd2','placeholder':'确认密码'}))

class SetInfoForm(forms.Form):
    username = forms.CharField()

class CommentForm(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={
        'cols':'60','rows':'6'
    }))

class SearchForm(forms.Form):
    keyword =forms.CharField(widget=forms.TextInput)