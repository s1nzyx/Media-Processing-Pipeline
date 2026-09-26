from rest_framework import serializers
from .models import MediaAsset, ProcessingTask

class ProcessingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingTask
        fields = ['id', 'step_name', 'status', 'details', 'created_at', 'updated_at']

class MediaAssetSerializer(serializers.ModelSerializer):
    tasks = ProcessingTaskSerializer(many=True, read_only=True)
    original_file_url = serializers.SerializerMethodField()
    processed_file_url = serializers.SerializerMethodField() # Убедитесь, что здесь нет опечаток

    class Meta:
        model = MediaAsset
        fields = [
            'id', 'original_filename', 'file_size', 'mime_type',
            'status', 'original_file', 'processed_file', 
            'original_file_url', 'processed_file_url', # Обязательно должно быть здесь
            'thumbnail', 'error_message', 'created_at', 'tasks'
        ]
        read_only_fields = ['id', 'status', 'file_size', 'mime_type', 'error_message', 'created_at', 'original_file']

    def get_original_file_url(self, obj):
        if obj.original_file:
            return obj.original_file.url
        return None

    def get_processed_file_url(self, obj):
        if obj.processed_file:
            return obj.processed_file.url
        return None