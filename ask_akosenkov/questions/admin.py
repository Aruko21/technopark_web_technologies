from django.contrib import admin
from questions.models import *

# login: admin
# password: BlueBear
# otherpass: MissArcadia

# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Like)