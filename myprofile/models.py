from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=255)  # This will store the dictionary key (title)
    content = models.TextField()  # This will store the dictionary value (news content)
    date = models.DateField()  # Timestamp for the news article

    def __str__(self):
        return self.title