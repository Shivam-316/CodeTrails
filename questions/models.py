from django.db import models
from trails.models import Trail
class Question(models.Model):
    ques = models.TextField(verbose_name='Question')
    asset = models.URLField(verbose_name='Asset Link ',null=True,blank=True)
    ans = models.CharField(max_length=600,verbose_name='Answer ')
    trail = models.ForeignKey(Trail,on_delete=models.CASCADE)
    identifier = models.CharField(max_length=2)

    def __str__(self):
        return self.identifier
