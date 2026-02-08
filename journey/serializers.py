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
        fields = ['week', 'feeling_state']

class BabyDataSerializer(serializers.Serializer):
    week_number = serializers.IntegerField()
    baby_image = serializers.URLField()
    baby_size = serializers.FloatField()
    baby_weight = serializers.FloatField()
    baby_analogy = serializers.CharField()
    baby_activity = serializers.CharField()
    baby_development = serializers.CharField()
    interesting_fact = serializers.CharField()

class MomDataSerializer(serializers.Serializer):
    week_number = serializers.IntegerField()  # ✅ No source='week_number'
    feelingsStates = serializers.SerializerMethodField()
    sensationDescr = serializers.CharField(source='mom_daily_tips')
    comfortTips = ComfortTipSerializer(many=True, source='comfort_tips')

    def get_feelingsStates(self, obj):
        return [f.feeling_state for f in obj.mom_feelings.all()]

class FullWeekDataSerializer(serializers.Serializer):
    week_number = serializers.IntegerField()
    days_to_childbirth = serializers.IntegerField()

    # ✅ Extract baby fields directly from WeekData
    baby = serializers.SerializerMethodField()

    momTip = serializers.SerializerMethodField()

    def get_baby(self, obj):
        return {
            'week_number': obj.week_number,
            'baby_image': obj.baby_image,
            'baby_size': obj.baby_size,
            'baby_weight': obj.baby_weight,
            'baby_analogy': obj.baby_analogy,
            'baby_activity': obj.baby_activity,
            'baby_development': obj.baby_development,
            'interesting_fact': obj.interesting_fact,
        }

    def get_momTip(self, obj):
        return {
            'dailyTip': getattr(obj, 'daily_tip', None),
            'comfortTip': ComfortTipSerializer(obj.comfort_tips.first()).data
                         if hasattr(obj, 'comfort_tips') and obj.comfort_tips.exists() else None
        }
