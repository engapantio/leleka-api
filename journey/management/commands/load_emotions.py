import json
import os
from django.core.management.base import BaseCommand
from diaries.models import Emotion

class Command(BaseCommand):
    help = 'Load pregnancy data from JSON files'

    def handle(self, *args, **options):
        # Clear existing data
        Emotion.objects.all().delete()

        loaded_weeks = 0

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
            f'   Emotions: {Emotion.objects.count()}'
        ))
