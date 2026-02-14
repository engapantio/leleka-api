import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from journey.models import WeekData

class Command(BaseCommand):
    help = 'Load mom states JSON into WeekData.sensationDescription'

    def handle(self, *args, **options):
        json_path = os.path.join(settings.BASE_DIR, 'lehlehka.mom_states.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'File not found: {json_path}'))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        loaded = 0
        for item in data:
            week_num = item['weekNumber']
            try:
                week_data = WeekData.objects.get(weekNumber=week_num)
                week_data.sensationDescr = item['feelings']['sensationDescr']
                week_data.save()
                loaded += 1
                self.stdout.write(f'✅ Loaded week {week_num}')
            except WeekData.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Skipped week {week_num} - no WeekData'))

        self.stdout.write(
            self.style.SUCCESS(f'Loaded {loaded}/{len(data)} weeks!')
        )
