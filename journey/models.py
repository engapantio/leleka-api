from django.db import models

class WeekData(models.Model):
    week_number = models.IntegerField(unique=True)
    days_to_childbirth = models.IntegerField(null=True, blank=True)
    
    # Baby data
    baby_image = models.URLField()
    baby_size = models.FloatField()
    baby_weight = models.FloatField()
    baby_analogy = models.CharField(max_length=255, blank=True, null=True)
    baby_activity = models.TextField()
    baby_development = models.TextField()
    interesting_fact = models.TextField()
    mom_daily_tips = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['week_number']
    
    def __str__(self):
        return f"Week {self.week_number}"

class MomFeeling(models.Model):
    week = models.ForeignKey(WeekData, on_delete=models.CASCADE, related_name='mom_feelings')
    feeling_state = models.CharField(max_length=255)
    
    class Meta:
        unique_together = ['week', 'feeling_state']


class ComfortTip(models.Model):
    week = models.ForeignKey(WeekData, related_name='comfort_tips', on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    tip = models.TextField()
    
    class Meta:
        unique_together = ['week', 'category']
