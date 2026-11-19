import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from notes.models import Category, Note, Tag


class Command(BaseCommand):
    help = "Заполняет базу тестовыми заметками"

    def add_arguments(self, parser):
        parser.add_argument("--notes", type=int, default=100_000)

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker("ru_RU")
        User = get_user_model()
        users = [User.objects.get_or_create(username=f"user{i}")[0] for i in range(20)]

        Category.objects.bulk_create(
            [Category(name=f"Категория {i}") for i in range(50)], ignore_conflicts=True
        )
        Tag.objects.bulk_create(
            [Tag(name=f"тег{i}") for i in range(200)], ignore_conflicts=True
        )

        categories = list(Category.objects.all())
        tags = list(Tag.objects.all())
        total = options["notes"]
        batch = 5000
        Through = Note.tags.through

        for start in range(0, total, batch):
            size = min(batch, total - start)
            notes = Note.objects.bulk_create([
                Note(
                    title=fake.sentence(nb_words=4)[:200],
                    text=fake.text(max_nb_chars=400),
                    is_done=random.random() < 0.3,
                    owner=random.choice(users),
                    category=random.choice(categories),
                )
                for _ in range(size)
            ])

            Through.objects.bulk_create([
                Through(note_id=note.pk, tag_id=tag.pk)
                for note in notes
                for tag in random.sample(tags, 3)
            ])

            self.stdout.write(f"Создано {start + size} из {total}")