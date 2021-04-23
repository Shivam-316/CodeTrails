from django.db import models
from django.contrib.auth.models import User
from questions.models import Question
class Profile(models.Model):
    def num_ques():
        return (Question.objects.all().count() - 1)//3 + 1

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    to_attempt = models.PositiveSmallIntegerField(verbose_name="Questions To Attempt ",default=num_ques)
    attempted_count = models.PositiveIntegerField(verbose_name="Questions Attempted ",default=0)
    score = models.PositiveIntegerField(default=0)
    time_details = models.TextField(verbose_name='Time Details ',default='')
    curr_ques_id = models.CharField(max_length=2,default='i0',verbose_name='Current Question At Identifier ')
    choosing_trail = models.BooleanField(default=False,verbose_name='Choosing A Trail ')


    def __str__(self):
        return f"{self.user.username}'s Profile"
