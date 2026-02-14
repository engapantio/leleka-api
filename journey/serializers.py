# journey/serializers.py
from rest_framework import serializers
from .models import WeekData, ComfortTip, MomFeeling

class ComfortTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComfortTip
        fields = ['category', 'tip']

class MomFeelingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MomFeeling
        fields = ['weekNumber', 'feelingState']

class BabyDataSerializer(serializers.Serializer):
    weekNumber = serializers.IntegerField()
    image = serializers.URLField()
    babySize = serializers.FloatField()
    babyWeight = serializers.FloatField()
    analogy = serializers.CharField()
    babyActivity = serializers.CharField()
    babyDevelopment = serializers.CharField()
    interestingFact = serializers.CharField()
    momDailyTips = serializers.SerializerMethodField()

    def get_momDailyTips(self, obj):
        return getattr(obj, 'momDailyTips', [])

class MomDataSerializer(serializers.Serializer):
    weekNumber = serializers.IntegerField()
    feelingsStates = serializers.SerializerMethodField()
    sensationDescr = serializers.CharField()
    comfortTips = ComfortTipSerializer(many=True)

    def get_feelingsStates(self, obj):
        return [f.feelingState for f in obj.momFeelings.all()]

class FullWeekDataSerializer(serializers.Serializer):
    weekNumber = serializers.IntegerField()
    daysToChildbirth = serializers.IntegerField()

    # ✅ Extract baby fields directly from WeekData
    baby = serializers.SerializerMethodField()

    momTip = serializers.SerializerMethodField()

    def get_baby(self, obj):
        return {
            'weekNumber': obj.weekNumber,
            'image': obj.image,
            'babySize': obj.babySize,
            'babyWeight': obj.babyWeight,
            'analogy': obj.analogy,
            'babyActivity': obj.babyActivity,
            'babyDevelopment': obj.babyDevelopment,
            'interestingFact': obj.interestingFact,
        }

    def get_momTip(self, obj):
        mom_tips = getattr(obj, 'momDailyTips', [])
        daily_tip = mom_tips[0] if mom_tips else "No tips available"
        return {
            'dailyTip': daily_tip,
            'comfortTip': ComfortTipSerializer(obj.comfortTips.first()).data
                         if hasattr(obj, 'comfortTips') and obj.comfortTips.exists() else None
        }
