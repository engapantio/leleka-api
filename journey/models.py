from django.db import models

class WeekData(models.Model):
    weekNumber = models.IntegerField(unique=True)
    daysToChildbirth = models.IntegerField(null=True, blank=True)

    # Baby data
    image = models.URLField()
    babySize = models.FloatField()
    babyWeight = models.FloatField()
    analogy = models.CharField(max_length=255, blank=True, null=True)
    babyActivity = models.TextField()
    babyDevelopment = models.TextField()
    interestingFact = models.TextField()
    momDailyTips = models.JSONField(default=list)
    sensationDescr = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['weekNumber']

    def __str__(self):
        return f"Week {self.weekNumber}"

class MomFeeling(models.Model):
    weekNumber = models.ForeignKey(WeekData, on_delete=models.CASCADE, related_name='momFeelings')
    feelingState = models.CharField(max_length=255)

    class Meta:
        # unique_together = ['weekNumber', 'feelingState']
        constraints = [
            models.UniqueConstraint(fields=['weekNumber', 'feelingState'], name='unique_week_feeling')
        ]


class ComfortTip(models.Model):
    weekNumber = models.ForeignKey(WeekData, related_name='comfortTips', on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    tip = models.TextField()

    class Meta:
        # unique_together = ['weekNumber', 'category']
        constraints = [
            models.UniqueConstraint(fields=['weekNumber', 'category'], name='unique_week_category')
        ]
