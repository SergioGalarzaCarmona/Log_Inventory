from django.db import models
from django.contrib.auth.models import User
from Users.models import Subprofile, TypeChanges

# Create your models here.


class BaseAuditModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ObjectsGroup(BaseAuditModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(
        default="default_object_group.jpg", upload_to="objectGroups_images"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    in_charge = models.ForeignKey(Subprofile, on_delete=models.CASCADE)
    description = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"


class Objects(BaseAuditModel):
    group = models.ForeignKey(ObjectsGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    stock = models.IntegerField()
    image = models.ImageField(default="default_object.jpg", upload_to="objects_images")
    description = models.TextField()
    in_charge = models.ForeignKey(Subprofile, on_delete=models.CASCADE)

    def available_stock(self, excluded_borrowing=None):
        from django.db.models import Sum, Q

        borrowed = (
            self.borrowings.filter(
                Q(completed=False) & ~Q(id=excluded_borrowing.id)
                if excluded_borrowing
                else Q(completed=False)
            ).aggregate(total=Sum("stock"))
        )["total"] or 0

        return self.stock - borrowed

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Object"
        verbose_name_plural = "Objects"


class TypeTransaction(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} Transaction Type"

    class Meta:
        verbose_name = "TypeTransaction"
        verbose_name_plural = "TypeTransactions"


class GroupObjectsChanges(models.Model):
    main_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="group_objects_main_user"
    )
    group_changed = models.ForeignKey(ObjectsGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="group_objects_user"
    )
    type_change = models.ForeignKey(TypeChanges, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(TypeTransaction, on_delete=models.CASCADE)
    object = models.ForeignKey(Objects, on_delete=models.CASCADE)
    in_charge = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="objects_in_charge"
    )
    stock_before = models.IntegerField()
    stock_after = models.IntegerField()
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.object.name} Transaction"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
