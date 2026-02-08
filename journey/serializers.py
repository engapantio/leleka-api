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
    week_number = serializers.IntegerField(source='week_number')
    baby_image = serializers.URLField(source='baby_image')
    baby_size = serializers.FloatField(source='baby_size')
    baby_weight = serializers.FloatField(source='baby_weight')
    baby_analogy = serializers.CharField(source='baby_analogy')
    baby_activity = serializers.CharField(source='baby_activity')
    baby_development = serializers.CharField(source='baby_development')
    interesting_fact = serializers.CharField(source='interesting_fact')

class MomDataSerializer(serializers.Serializer):
    weekNumber = serializers.IntegerField()  # ✅ No source='week_number'
    feelingsStates = serializers.SerializerMethodField()
    sensationDescr = serializers.CharField(source='daily_tip')  # ✅ Different name OK
    comfortTips = ComfortTipSerializer(many=True)

    def get_feelingsStates(self, obj):
        return [f.feeling_state for f in obj.mom_feelings.all()]  # ✅ Fixed relation

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
