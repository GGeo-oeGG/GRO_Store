from itertools import islice

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Генерирует последовательность по заданному количеству элементов'

    def add_arguments(self, parser):
        parser.add_argument(
            'n',
            type=int,
            help='Количество элементов последовательности'
        )

    def get_elements(self, n: int):
        """Возвращает список из первых n элементов последовательности 1, 2, 2, 3, 3, 3, ...
        Если n < 0, возвращает 0.
        """
        if n < 0:
            return 0

        def _generator():
            num = 1
            while True:
                yield from [num] * num
                num += 1

        return list(islice(_generator(), n))

    def handle(self, *args, **options):
        n = options['n']
        result = self.get_elements(n)
        self.stdout.write(f'Лови списочек! \n {result}')
