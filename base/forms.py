from django.forms import ModelForm
from base.models import Room, Member
from django import forms

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"

class MemberForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = Member
        fields=('__all__')