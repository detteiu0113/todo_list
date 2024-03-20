from django.core.management.base import BaseCommand
from django.db import transaction
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'モデルを自動で作成します'

    def handle(self, *args, **options):
        with transaction.atomic():
            def create_user(username, last_name, first_name):
                user = CustomUser.objects.create(
                    username=username,
                    last_name=last_name,
                    first_name=first_name,
                    is_staff=True,
                    is_superuser=True,
                )
                user.set_password('detteiu')
                user.save()
            
            if not CustomUser.objects.exists():

                create_user('yuto', '清水', '優人')
                create_user('haruki', '泥谷', '陽輝')
                create_user('keito', '藤尾', '景虎')

                self.stdout.write(self.style.SUCCESS('全てのユーザーの作成が終了しました'))
            