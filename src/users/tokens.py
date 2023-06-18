from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class PasswordTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return (
            text_type(user.pk) + user.password + text_type(login_timestamp) + text_type(timestamp)
        )

password_token_gen = PasswordResetTokenGenerator()