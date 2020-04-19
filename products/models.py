from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class Product(models.Model):
    title = models.CharField(max_length=255, null=False, default="Title not parsed")    
    pub_date = models.DateTimeField(default=timezone.datetime.now)
    body = models.TextField(null=False, default="No description was supplied")
    url = models.TextField(null=False)    
    image = models.ImageField(upload_to="images/")
    icon = models.ImageField(upload_to="images/")        
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def votes_total(self):
        return ProductVotes.objects.filter(product__id=self.id).count()

    def summary(self):
        text=""
        max_words=30
        count=0
        words=self.body.split(' ')
        
        if len(self.body.split(' ')) <= max_words:
            return self.body
        else:
            while count < max_words:
                text = "%s %s" % (text, words[count])
                count += 1
            return "{}...".format(text)

    def pub_date_pretty(self):
        return self.pub_date.strftime("%b %d %Y")


class ProductVotes(models.Model):
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)