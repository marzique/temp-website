from django.db import models

from django_countries.fields import CountryField


class Player(models.Model):
 
    NUMBER_CHOICES = zip(range(1, 100), range(1, 100)) # 1-99

    GK = 'goalkeeper'
    DF = 'defender'
    MF = 'midfielder'
    ST = 'striker'
    MG = 'manager'
    POSITION_CHOICES = (
        (GK, 'Goalkeeper'),
        (DF, 'Defender'),
        (MF, 'Midfielder'),
        (ST, 'Striker'),
        (MG, 'Manager')
    )

    first_name = models.CharField(max_length=100, null=False, blank=False)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    number = models.PositiveIntegerField(choices=NUMBER_CHOICES, db_index=True, null=True, blank=True)
    position = models.CharField(choices=POSITION_CHOICES, max_length=200, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    photo = models.ImageField(upload_to='squad/')
    captain = models.BooleanField(default=None, unique=True, null=True)
    nationality = CountryField()

    def __str__(self):
        
        return f'{self.number}. {self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        # make captain bool True only for one Player
        if self.captain is False:
            self.captain = None
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['number']