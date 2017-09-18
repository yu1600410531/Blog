# -*- coding: utf-8 -*-
from rest_framework import serializers
import models

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Article
        fields = ['title', 'author', 'content','column','author','user', ' pub_date']

