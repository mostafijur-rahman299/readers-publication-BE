from django.core.management.base import BaseCommand
from core.models import Country, State, City, Thana, Union
from utils.general_data import BD_LOCATION_DATA

class Command(BaseCommand):
    help = 'Import real Bangladesh location data using a Python dictionary'

    def handle(self, *args, **kwargs):
        self.stdout.write("Importing Bangladesh location data...")

        country, _ = Country.objects.get_or_create(
            code=BD_LOCATION_DATA["code"],
            defaults={
                "name": BD_LOCATION_DATA["name"],
                "name_bn": BD_LOCATION_DATA["name_bn"]
            }
        )

        for division in BD_LOCATION_DATA["divisions"]:
            state, _ = State.objects.get_or_create(
                name=division["name"],
                name_bn=division["name_bn"],
                country=country
            )

            for district in division["districts"]:
                city, _ = City.objects.get_or_create(
                    name=district["name"],
                    name_bn=district["name_bn"],
                    state=state
                )

                for thana_data in district["thanas"]:
                    thana, _ = Thana.objects.get_or_create(
                        name=thana_data["name"],
                        name_bn=thana_data["name_bn"],
                        city=city
                    )

                    for union_data in thana_data["unions"]:
                        Union.objects.get_or_create(
                            name=union_data["name"],
                            name_bn=union_data["name_bn"],
                            thana=thana
                        )

        self.stdout.write(self.style.SUCCESS("✅ Bangladesh location data imported successfully."))