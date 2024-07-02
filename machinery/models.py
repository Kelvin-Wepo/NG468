from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.files.storage import default_storage as storage
from PIL import Image


class Customer(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Customer"

    def get_absolute_url(self):
        return reverse('single_customer', kwargs={"id": self.id})

    @property
    def get_person(self):
        return reverse('delete_customer', kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        if not self.username:
            return

        super(Customer, self).save(*args, **kwargs)
        if self.image:
            size = 300, 300
            image = Image.open(self.image)
            image.thumbnail(size, Image.LANCZOS)
            fh = storage.open(self.image.name, "w")
            format = 'png'
            image.save(fh, format)
            fh.close()


class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Admin"


class PlantOperator(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=100, null=False)
    level = [
        ('Junior', 'Junior'),
        ('Mid-Level', 'Mid-Level'),
        ('Expert', 'Expert')
    ]
    skill = models.CharField(max_length=100, choices=level, null=False)
    salary = models.PositiveIntegerField(null=True)
    hired = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @property
    def get_id(self):
        return f"{self.username.id}"

    @property
    def get_person(self):
        return reverse('delete_plant_operator', kwargs={"id": self.id})

    def get_absolute_url(self):
        return reverse('single_plant_operator', kwargs={"id": self.id})

    class Meta:
        verbose_name_plural = "PlantOperator"

    def save(self, *args, **kwargs):
        if not self.username:
            return

        super(PlantOperator, self).save(*args, **kwargs)
        if self.image:
            size = 300, 300
            image = Image.open(self.image)
            image.thumbnail(size, Image.LANCZOS)
            fh = storage.open(self.image.name, "w")
            format = 'png'
            image.save(fh, format)
            fh.close()


class Machinery(models.Model):
    MACHINERY_TYPES = [
        ('Water Pump', 'Water Pump'),
        ('Sewage Pump', 'Sewage Pump'),
        ('Treatment Plant Equipment', 'Treatment Plant Equipment'),
        ('Pipe Laying Machine', 'Pipe Laying Machine'),
        ('Jetting Machine', 'Jetting Machine'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=MACHINERY_TYPES)
    description = models.TextField()
    availability = models.BooleanField(default=True)
    operator = models.ForeignKey(PlantOperator, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Machinery"


class Request(models.Model):
    machinery = models.ForeignKey(Machinery, on_delete=models.CASCADE, null=True)
    problem_description = models.CharField(max_length=1000, null=False)
    date = models.DateField(auto_now=True)
    cost = models.PositiveIntegerField(null=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
    plant_operator = models.ForeignKey('PlantOperator', on_delete=models.CASCADE, null=True)

    final = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Repairing', 'Repairing'),
        ('Repairing Done', 'Repairing Done'),
        ('Released', 'Released')
    ]
    status = models.CharField(max_length=100, choices=final, default='Pending', null=True)

    def __str__(self):
        return f"{self.machinery} - {self.problem_description}"

    class Meta:
        ordering = ('-date',)
        verbose_name_plural = "Request"


class Attendance(models.Model):
    plant_operator = models.ForeignKey('PlantOperator', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now, blank=True)
    status = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    present_status = models.CharField(max_length=20, choices=status, default='No')

    def __str__(self):
        return f"{self.plant_operator} - {self.present_status}"

    class Meta:
        verbose_name_plural = "Attendance"


class Feedback(models.Model):
    username = models.CharField(max_length=40)
    message = models.CharField(max_length=500)
    date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name_plural = "Feedback"


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=100, null=False, blank=False)
    message = models.TextField(max_length=5000)

    def __str__(self):
        return f'{self.name} - {self.email}'

    class Meta:
        verbose_name_plural = "Contact"


class News(models.Model):
    email = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name_plural = "News"


class About(models.Model):
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = "About"
