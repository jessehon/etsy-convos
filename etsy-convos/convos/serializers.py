# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *

class ConvoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convo

class ConvoThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvoThread
