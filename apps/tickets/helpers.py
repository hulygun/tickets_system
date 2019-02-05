def user_is_author(instance, user):
    return instance.author == user


def user_is_performer(instance, user):
    return instance.performer == user


def can_processed(instance):
    return not instance.__class__.objects.filter(
        performer_id=instance.performer_id,
        state='processed'
    ).exclude(id=instance.id).exists()
