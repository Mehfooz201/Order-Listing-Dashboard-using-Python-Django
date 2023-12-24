# cdlapp/hashers.py
from django.contrib.auth.hashers import BasePasswordHasher

class PlainTextPasswordHasher(BasePasswordHasher):
    algorithm = 'plaintext'

    def verify(self, password, encoded):
        return password == encoded

    def encode(self, password, salt):
        return password

    def safe_summary(self, encoded):
        return {
            _('algorithm'): self.algorithm,
        }
