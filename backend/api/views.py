from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MediaAsset
from .serializers import MediaAssetSerializer

class MediaAssetViewSet(viewsets.ModelViewSet):
    queryset = MediaAsset.objects.all().order_by('-created_at')
    serializer_class = MediaAssetSerializer

    def perform_create(self, serializer):
        # Получаем загруженный файл из запроса
        uploaded_file = self.request.FILES.get('file') # Или 'processed', в зависимости от названия поля в сериализаторе
        
        # Если файл есть, берем его размер в байтах
        file_size = uploaded_file.size if uploaded_file else 0

        # Сохраняем объект, передавая рассчитанный размер
        serializer.save(file_size=file_size)

    @action(detail=True, methods=['post'])
    def trigger_processing(self, request, pk=None):
        #endpoint для ручаного/тестового запуска обработки файла   

        asset = self.get_object()
        if asset.status == MediaAsset.Status.PROCESSING:
            return Response(
            {"error": "Файл уже находиться в процессе обработки."},
            status=status.HTTP_400_BAD_REQUEST
            )

        process_media_file_task.delay(str(asset.id))
        #здесь в будущем мы будем дергать temporal workflow

        return Response(
            {
                "message": f"Задача для файла {asset.original_filename} успешно отправлена в очередь Celery.",
                "asset_id": str(asset.id)
            },
            status=status.HTTP_202_ACCEPTED
        )