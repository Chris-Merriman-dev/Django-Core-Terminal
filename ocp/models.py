'''
    Created By : Christian Merriman
    Purpose : Objets used for our database
'''
import random
from django.db import models
from django.contrib.auth.models import AbstractUser

#our users data
class User(AbstractUser):
    #fun id for ocp member
    employee_id = models.CharField(
        max_length=14, 
        unique=True, 
        blank=True,
        help_text="Format: OCP-XXXXXX"
    )
    
    #different clearance levels users can have
    CLEARANCE_CHOICES = [
        (1, 'Level 1: Guest'),
        (2, 'Level 2: Employee'),
        (3, 'Level 3: Mid-Management'),
        (4, 'Level 4: Senior Executive'),
        (5, 'Level 5: OCP Board Member'),
    ]
    access_level = models.IntegerField(choices=CLEARANCE_CHOICES, default=1)

    #this will automatically create our OCP id
    def save(self, *args, **kwargs):
        if not self.employee_id:
            #Look at the most recently created user
            last_user = User.objects.all().order_by('id').last()
            
            if not last_user or not last_user.employee_id:
                #First ever OCP employee Richard (Dick) Jones
                self.employee_id = "OCP-100001"
            else:
                #extract the number from "OCP-100005", add 1, and put it back
                last_id_int = int(last_user.employee_id.split('-')[1])
                if last_id_int < 999999:
                    self.employee_id = f"OCP-{last_id_int + 1}"
                else:
                    raise ValueError("OCP Personnel Capacity Reached. Directive 4: No further hires permitted.")
        
        super().save(*args, **kwargs)

#stores Flux .1 Image Generations linked to OCP Personnel
class Asset(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assets")
    image = models.ImageField(upload_to="generations/")
    prompt = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Technical data for Flux/ComfyUI tracking
    seed = models.CharField(max_length=255, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    
    # Executive Approvals (Likes)
    approvals = models.ManyToManyField(User, related_name="approved_assets", blank=True)

    class Meta:
        ordering = ['-timestamp']

#feedback on the users images 
class Comment(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

#logs of LLM chat interactions with ED-209
class Directive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_logs")
    user_query = models.TextField()
    ed209_response = models.TextField()
    clearance_at_time = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
