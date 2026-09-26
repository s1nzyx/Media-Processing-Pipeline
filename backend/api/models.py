from django.db import models
import uuid
from django.contrib.auth.models import User

class MediaAsset(models.Model):
    class Status(models.TextChoices):
        UPLOADED = 'uploaded', 'загружен'
        PROCESSING = 'processing', 'в обработке'
        COMPLETED = 'completed', 'готов'
        FAILED = 'failed', 'Ошибка'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media_assets', null=True, blank=True)

    original_filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField(help_text="Размер в байтах")
    mime_type = models.CharField(max_length=100, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UPLOADED
    )
#пути ссылки на файлы в s3 (minIO)
    original_file = models.FileField(upload_to='originals/')
    processed_file = models.FileField(upload_to='processed/', blank=True, null=True)
    thumbnail = models.FileField(upload_to='thumbnails/', blank=True, null=True)

    error_message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.original_filename} ({self.status})"

class ProcessingTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name='tasks')

    step_name = models.CharField(max_length=100, help_text="например: resize, watermarking, hls_convert")
    status = models.CharField(max_length=20, default='pending') #pending running, success, failed
    details = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task {self.step_name} for {self.asset.original_filename} - {self.status}"