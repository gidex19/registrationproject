from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from PIL import Image
from django.conf import settings

class Customuser(AbstractUser):
    submitted = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class Bio(models.Model):
    gender_choices = (('male', 'Male'), ('female', 'Female'))
    relationship_list = (('father','Father'), ('mother','Mother'), ('brother', 'Brother'), ('sister', 'Sister'), ('uncle','Uncle'))
    user = models.OneToOneField(Customuser, on_delete=models.CASCADE)
    first_name = models.CharField( max_length=20)
    last_name = models.CharField(max_length=20 )
    middle_name = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10, choices=gender_choices)
    date_of_birth = models.DateField()
    hobbies = models.TextField(max_length=80 )
    nok1_name = models.CharField(max_length=32)
    nok1_phone = models.CharField(max_length=11)
    nok1_relationship = models.CharField(max_length=12, choices=relationship_list)
    nok2_name = models.CharField(max_length=32 )
    nok2_phone = models.CharField(max_length=11)
    nok2_relationship = models.CharField(max_length=12, choices=relationship_list)

    #academic information
    primary = models.CharField(max_length=80)
    secondary = models.CharField(max_length=80)
    tertiary = models.CharField(max_length=80)

    #Upload Documents
    passport = models.ImageField(upload_to= 'passport')
    o_level = models.ImageField(upload_to='o_level')
    birth_cert = models.ImageField(upload_to='birth_cert')
    indegeneship_cert = models.ImageField(upload_to='indegene')
    degree_cert = models.ImageField(upload_to='degree')

    #referees
    ref1_name = models.CharField(max_length=35)
    ref1_phone = models.CharField(max_length=11)
    ref1_occupation = models.CharField(max_length=35)

    ref2_name = models.CharField(max_length=35)
    ref2_phone = models.CharField(max_length=11)
    ref2_occupation = models.CharField(max_length=35)
    submitted = models.BooleanField(default=False)


    def __str__(self):
        return ('Bio for {}'.format(self.user.username))

    def get_absolute_url(self):
        return reverse('success')

    def save(self,*args, **kwargs):
        super().save()

        large = [self.o_level, self.birth_cert, self.indegeneship_cert, self.degree_cert]
        for i in large:
            img = Image.open(i.path)
            if img.height > 700 or img.width > 550:
                output_size = (700, 550)
                img.thumbnail(output_size)
                img.save(i.path)

        img = Image.open(self.passport.path)
        if img.height > 180 or img.width > 150:
            output_size = (180, 150)
            img.thumbnail(output_size)
            img.save(self.passport.path)

    class Meta:
        ordering = ('-last_name',)
