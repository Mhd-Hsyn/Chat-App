from django.db import models
import uuid

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now= False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add= False, blank=True, null=True)

    class Meta:
        abstract = True

class User(BaseModel):
    fname= models.CharField(max_length=50, default= "")
    lname= models.CharField(max_length=50, default= "")
    profile= models.ImageField(upload_to="Users/", default="Users/dummy.png")
    email = models.CharField(max_length=150, unique= True)
    password = models.TextField()

    def __str__(self):
        return self.email

class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null= True)
    token = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, auto_now=False)

    def __str__(self) :
        return str(self.user)

class Chats(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_name= models.CharField(max_length=50)
    created_by= models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_now= False, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Message(BaseModel):
    chatid = models.ForeignKey(Chats, on_delete=models.CASCADE)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.message
