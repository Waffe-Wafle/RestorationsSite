from django.db import models
from Site.settings import MONEY_SYMBOL
from django.core.validators import MinValueValidator, ValidationError


def restoration_status_validate(value):
    STATUS = ['actual', 'deleted']
    if value not in STATUS:
        raise ValidationError(f"Status shoulde be one of {STATUS}")


# Dfault blank and null are false.
class RestoreWork(models.Model):
    restore_id = models.BigAutoField(db_column='restore_ID', primary_key=True)
    name = models.CharField(max_length=70)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
                              # default='static/Restorations/src/card_img_placeholder.jpg'
    total_sum = models.IntegerField(validators=[
        MinValueValidator(1)
    ])
    status = models.CharField(max_length=7, validators=[
        restoration_status_validate
    ])

    class Meta:
        managed = True
        db_table = 'RestoreWorks'

    def __str__(self):
        got_sum = Donation.objects.filter(restore_id=self.restore_id).aggregate(sum=models.Sum('sum'))['sum']
        return f'{self.name} ({got_sum if got_sum else 0} / {self.total_sum}) ' + MONEY_SYMBOL


class Donater(models.Model):
    donater_id = models.BigAutoField(db_column='donater_ID', primary_key=True)
    login = models.CharField(unique=True, max_length=5, )
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(db_column='description', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Donaters'

    def __str__(self):
        return self.login


class Donation(models.Model):
    donation_id = models.BigAutoField(db_column='donation_ID', primary_key=True)
    restore_id = models.ForeignKey(RestoreWork, models.CASCADE, db_column='restore_ID')
    donater_id = models.ForeignKey(Donater, models.DO_NOTHING, db_column='donater_ID')
    sum = models.IntegerField(validators=[
        MinValueValidator(1)
    ])
    card_number = models.BigIntegerField()
    payment_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Donations'

    def __str__(self):
        return f'{Donater.objects.get(donater_id=self.donater_id_id).login}: {self.sum}' + MONEY_SYMBOL \
             + f' -> {RestoreWork.objects.get(restore_id=self.restore_id_id).name}'




