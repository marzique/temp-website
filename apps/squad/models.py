from datetime import datetime, date

from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

from slugify import slugify
from django_countries.fields import CountryField



class Player(models.Model):
 
    NUMBER_CHOICES = zip(range(1, 100), range(1, 100)) # 1-99

    GK = 1
    DF = 2
    MF = 3
    ST = 4
    MG = 5
    POSITION_CHOICES = (
        (GK, 'Воротар'),
        (DF, 'Захисник'),
        (MF, 'Півзахисник'),
        (ST, 'Нападник'),
        (MG, 'Тренер')
    )

    first_name = models.CharField(max_length=100, null=False, blank=False)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    number = models.PositiveIntegerField(choices=NUMBER_CHOICES, db_index=True, null=True, blank=True, unique=True)
    position = models.PositiveIntegerField(choices=POSITION_CHOICES, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    photo = models.ImageField(upload_to='squad/')
    captain = models.BooleanField(default=None, unique=True, null=True)
    nationality = CountryField()
    name_slug = models.SlugField(max_length=200, unique=True, null=True)
    legend = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return f'{self.number}. {self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        # make slug from first and last names
        self.name_slug = '-'.join((slugify(self.first_name), slugify(self.last_name)))
        if str(self.number).isdigit():
            self.name_slug += f'-{self.number}'
        else:
            self.name_slug += f'-{self.pk}'

        # make captain bool True only for one Player
        if self.captain is False:
            self.captain = None
        super().save(*args, **kwargs)

    @property
    def years(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)) 

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['number']

    @property
    def position_ukranian(self):
        positions = {
            'goalkeeper': 'Вр',
            'defender': 'Зх',
            'midfielder': 'Цп',
            'striker': 'Нп',
            'manager': 'Тр'
        }
        return positions[self.position]


class Squad(models.Model):
    pitch_html = models.TextField()
    slug = models.SlugField(max_length=30, blank=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        blank=False, 
        null=True
    )
    created_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.slug = get_random_string(30)
            super().save(*args, **kwargs)
        except IntegrityError:
            self.save(*args, **kwargs)
