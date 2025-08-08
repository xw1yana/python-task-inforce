from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    date = models.DateField()
    items = models.TextField(help_text="A simple text list with menu items")

    class Meta:
        unique_together = ("restaurant", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"


class Vote(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="votes")
    created_at = models.DateTimeField(auto_now_add=True)
    vote_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "vote_date"], name="unique_employee_vote_per_day"
            )
        ]

    def save(self, *args, **kwargs):
        if not self.vote_date:
            self.vote_date = self.menu.date
        super().save(*args, **kwargs)
