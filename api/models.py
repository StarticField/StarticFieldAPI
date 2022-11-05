import hashlib
from django.core import validators
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
import datetime
import random
import string
# Create your models here.

degree_choices = [
    ("B.Tech", "B.Tech"),("B.Arc", "B.Arc"),("B.Des", "B.Des"),("BCA", "BCA"),
    ("B.Sc", "B.Sc"),("B.A", "B.A"),("B.Com", "B.Com"),("BBA", "BBA"),
    ("B.E", "B.E"),("M.Tech", "M.Tech"),("M.Des", "M.Des"),("MCA", "MCA"),
    ("M.Sc", "M.Sc"),("M.A", "M.A"),("M.Com", "M.Com"),("M.A", "M.A"),
    ("MBA", "MBA"),("M.S", "M.S"),("LLB", "LLB"),("B.S(Eco)", "B.S(Eco)"),
] 

def generate_code():
    length=6
    while True:
        code = ''.join(random.choices(string.ascii_uppercase,k=length))
        break
    return code

class Profile(models.Model):
    slug = models.CharField(editable=False, default=generate_code, max_length=50)
    full_name = models.CharField(null=True, blank=True, max_length=50)
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)#
    college = models.CharField(null=True, blank=True, max_length=100)#
    skills = models.CharField(null=True, blank=True, max_length=50)#
    pursuing = models.CharField(null=True, default="None", max_length=50, choices=degree_choices)#
    field = models.CharField(null=True, blank=True, max_length=50)#
    linkedin = models.URLField(max_length=200, null=True, blank=True, default="https://www.linkedin.com/")# links
    github = models.URLField(max_length=200, null=True, blank=True, default="https://www.github.com/")# links
    instagram = models.URLField(max_length=200, null=True, blank=True, default="https://www.instagram.com/")# links
    points = models.IntegerField(default=0)
    mobile = models.CharField(null=False, blank=True, max_length=50)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
status_choices = [
    ("Not Started", "Not Started"), ("Pending", "Pending"),
    ("Under Review", "Under Review"), ("Cleared", "Cleared"),
    ("Rejected", "Rejected")
]

class CTOHuntProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    max_round_cleared = models.IntegerField(default=0)
    round1Status = models.CharField(default="Not Started", max_length=50, choices=status_choices)
    round2Status = models.CharField(default="Not Started", max_length=50, choices=status_choices)
    round3Status = models.CharField(default="Not Started", max_length=50, choices=status_choices)
    result = models.CharField(default="Rejected", max_length=200)

    def __str__(self):
        max_cleared = ["None", "Round 1", "Round 2", "Round 3"][self.max_round_cleared]
        return f"{self.user.username} cleared {max_cleared}"

class MockPitchProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round1Status = models.CharField(default="Not Started", max_length=50, choices=status_choices)
    round2Status = models.CharField(default="Not Started", max_length=50, choices=status_choices)
    round3Status = models.CharField(default="Not Started", max_length=50, choices=status_choices)
    round4Status = models.CharField(default="Not Started", max_length=50, choices=status_choices)
    result = models.CharField(default="Rejected", max_length=200)

    def __str__(self):
        # max_cleared = ["None", "Round 1", "Round 2", "Round 3"][self.round_cleared]
        return self.user.username+" "+("selected" if self.selection_status else "rejected")