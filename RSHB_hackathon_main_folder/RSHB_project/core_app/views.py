from django.shortcuts import render
from .models import RobotCard
from django.views.generic import ListView

# Create your views here.


class RobotCardList(ListView):
    model = RobotCard
    template_name = 'default.html'
    context_object_name = 'robot_card_list'

