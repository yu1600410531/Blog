# -*- coding: utf-8 -*-

from django import forms

class LoginForm(forms.Form):
    uid =forms.CharField(widget=forms.TextInput(attrs={'labels':'用户名','class':'form-control', 'id':'uid', 'placeholder':'用户名'}))
    pwd = forms.CharField(widget=forms.PasswordInput(attrs={'labels':'密码','class':'form-control', 'id':'pwd','placeholder':'密码'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=100,
                               widget=forms.TextInput(attrs={'id':'username', 'onblur':'authentication()'}))
    # onblur 鼠标离开这个元素执行的方法
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

class SetInfoForm(forms.Form):
    username = forms.CharField()

class CommentForm(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={
        'cols':'60','rows':'6'
    }))

class SearchForm(forms.Form):
    keyword =forms.CharField(widget=forms.TextInput)