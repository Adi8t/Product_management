from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from app.models import Product, Category, AuditLog

@receiver(post_save)
def create_audit_log_on_save(sender, instance, created, **kwargs):
    if sender.__name__ == "AuditLog":
        return  # apna hi log skip karega

    action = "CREATE" if created else "UPDATE"
    AuditLog.objects.create(
        user=getattr(instance, "created_by", None),  # agar model me hai to lega
        action=action,
        model_name=sender.__name__,
        object_id=instance.pk,
    )


@receiver(post_delete)
def create_audit_log_on_delete(sender, instance, **kwargs):
    if sender.__name__ == "AuditLog":
        return

    AuditLog.objects.create(
        user=getattr(instance, "created_by", None),
        action="DELETE",
        model_name=sender.__name__,
        object_id=instance.pk,
    )
