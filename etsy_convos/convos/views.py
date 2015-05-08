# -*- coding: utf-8 -*-
from rest_framework import viewsets
from .models import *
from .serializers import *

class ConvoViewSet(viewsets.ModelViewSet):
    queryset = Convo.objects.all()
    serializer_class = ConvoSerializer
