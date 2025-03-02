# users/models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Team(models.Model):
    team_name = models.CharField(max_length=50, primary_key=True)
    team_leader = models.CharField(max_length=50)
    team_leader_email = models.EmailField(unique=True)
    members_count = models.PositiveIntegerField(default=1)
    member_emails = models.TextField(help_text="Comma-separated emails of all members")
    password_hash = models.CharField(max_length=128)  # Store hashed password

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def save(self, *args, **kwargs):
        emails = set(self.member_emails.split(',')) | {self.team_leader_email}
        self.member_emails = ','.join(emails)  # Ensure leader is included in members
        super().save(*args, **kwargs)
