from django.db import models
from datetime import date

# Create your models here.
class Publication(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE, related_name='publications')
    title = models.CharField('Title', max_length=255)
    text = models.TextField('Text', blank=True, null=True)
    image = models.ImageField('Image', blank=True, null=True)
    pub_date = models.DateField('Pub Date', default=date.today)
    isVisible = models.BooleanField('Is Visible', default=True)

    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'


    def __str__(self) -> str:
        return f'{self.title} {self.author.username}'


    def __repr__(self) -> str:
        return f'<Publication> {self.__str__()}'
    
    

class Comment(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='pub_comments')
    pub_date = models.DateField('Pub Date')
    publication = models.ForeignKey('publications.Publication', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Text')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    
    def __str__(self) -> str:
        return f'{self.publication.title} {self.author.username}'
    

    def __repr__(self) -> str:
        return f'<Comment> {self.__str__()}'