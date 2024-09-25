from users.models import User
import os
print(os.environ)
username = os.environ.get('SU_USERNAME', 'admin')
email = os.environ.get('SU_EMAIL', 'admin@site.com')
password = os.environ.get('SU_PASSWORD', 'password')
print(username, email, password)

user = User.objects.create(username=username, email=email, role="superuser")
user.set_password(password)
user.is_superuser = True
user.is_staff = True
user.save()
