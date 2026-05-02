import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

MODELS_LIST = ['Category', 'SubCategory', 'ProductImages']


@receiver(post_delete)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """ Удаление связанных изображений моделей. """

    if sender.__name__ in MODELS_LIST:
        if hasattr(instance, 'image'):
            image_field = getattr(instance, 'image')
            if image_field:
                image_field.delete(save=False)


@receiver(pre_save)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """ Удаление старого изображения при загрузке нового. """

    if sender.__name__ in MODELS_LIST and hasattr(instance, 'image'):

        if not instance.pk:
            return

        try:
            old_object = sender.objects.get(pk=instance.pk)
            old_image = old_object.image
        except sender.DoesNotExist:
            return

        new_image = instance.image

        if old_image and old_image != new_image:
            if os.path.isfile(old_image.path):
                old_image.delete(save=False)
