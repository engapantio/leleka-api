import json
import os
from django.core.management.base import BaseCommand
from journey.models import WeekData, MomFeeling, ComfortTip
from diaries.models import Emotion

class Command(BaseCommand):
    help = 'Load pregnancy data from JSON files'

    def handle(self, *args, **options):
        # Clear existing data
        WeekData.objects.all().delete()
        MomFeeling.objects.all().delete()
        ComfortTip.objects.all().delete()
        Emotion.objects.all().delete()

        loaded_weeks = 0

        # 1. BABY DATA (most important)
        baby_file = 'lehlehka.baby_states.json'
        if os.path.exists(baby_file):
            self.stdout.write('📁 Loading baby_states.json...')
            with open(baby_file, 'r', encoding='utf-8') as f:
                baby_data = json.load(f)

            for item in baby_data:
                try:
                    WeekData.objects.create(
                        weekNumber=item['weekNumber'],
                        image=item['image'],
                        babySize=item['babySize'],
                        babyWeight=item['babyWeight'],
                        analogy=item.get('analogy', ''),
                        babyActivity=item['babyActivity'],
                        babyDevelopment=item['babyDevelopment'],
                        interestingFact=item['interestingFact'],
                        momDailyTips=item.get('momDailyTips', []),
                        daysToChildbirth=max(0, 280 - (item['weekNumber'] * 7)),
                    )
                    loaded_weeks += 1
                except KeyError as e:
                    self.stdout.write(self.style.ERROR(f'Missing key in week {item.get("weekNumber")}: {e}'))

            self.stdout.write(self.style.SUCCESS(f'✅ {loaded_weeks} weeks loaded'))
        else:
            self.stdout.write(self.style.ERROR(f'❌ {baby_file} not found!'))

        # 2. MOM DATA (links to weeks)
        mom_file = 'lehlehka.mom_states.json'
        if os.path.exists(mom_file) and WeekData.objects.exists():
            self.stdout.write('📁 Loading mom_states.json...')
            with open(mom_file, 'r', encoding='utf-8') as f:
                mom_data = json.load(f)

            loaded_mom = 0
            for item in mom_data:
                try:
                    weekNumber = WeekData.objects.get(weekNumber=item['weekNumber'])

                    # Feelings
                    for state in item['feelings']['states']:
                        MomFeeling.objects.get_or_create(weekNumber=weekNumber, feelingState=state)

                    # Tips
                    for tip in item['comfortTips']:
                        ComfortTip.objects.get_or_create(
                            weekNumber=weekNumber, category=tip['category'], defaults={'tip': tip['tip']}
                        )
                    loaded_mom += 1
                except WeekData.DoesNotExist:
                    pass
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Skipped mom week {item["weekNumber"]}: {e}'))

            self.stdout.write(self.style.SUCCESS(f'✅ {loaded_mom} mom weeks linked'))
        else:
            self.stdout.write(self.style.WARNING('❌ Mom file missing or no weeks'))

        # 3. EMOTIONS
        emotion_file = 'lehlehka.emotions.json'
        if os.path.exists(emotion_file):
            self.stdout.write('📁 Loading emotions.json...')
            with open(emotion_file, 'r', encoding='utf-8') as f:
                emotions_data = json.load(f)

            loaded_emotions = 0
            for item in emotions_data:
                Emotion.objects.get_or_create(title=item['title'])
                loaded_emotions += 1

            self.stdout.write(self.style.SUCCESS(f'✅ {loaded_emotions} emotions loaded'))
        else:
            self.stdout.write(self.style.WARNING('❌ Emotions file missing'))

        # FINAL STATUS
        self.stdout.write(self.style.SUCCESS(
            f'\n🎉 SUMMARY:\n'
            f'   Weeks: {WeekData.objects.count()}\n'
            f'   Tips: {ComfortTip.objects.count()}\n'
            f'   Feelings: {MomFeeling.objects.count()}\n'
            f'   Emotions: {Emotion.objects.count()}'
        ))
