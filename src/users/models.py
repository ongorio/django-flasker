from django.db import models

from pathlib import Path


def upload_handler(instance, filename) -> str:
    """
    Upload Handler

    Creates the path and name for the UserExtension profile_pic
    The result is store in the media directory specified on the
    settings.py file.
    """
    ext = Path(filename).suffix
    res = Path() / 'profilepics' / f'{instance.user.username}.{ext}'
    return str(res)
    


class UserExtension(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='extension')
    birthdate = models.DateField('Birth Date')
    profile_pic = models.ImageField('Profile Pic', upload_to=upload_handler, null=True, blank=True)


    def __str__(self) -> str:
        return f'{self.user.username}'


    def __repr__(self) -> str:
        return f'<User Extension> {self.__str__()}'


    def delete(self, *args, **kwargs):
        img = Path(self.profile_pic.path)

        if img.exists():
            img.unlink()
        
        super().delete()