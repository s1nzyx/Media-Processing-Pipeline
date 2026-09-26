import time
from celery import shared_task
from .models import MediaAsset, ProcessingTask

@shared_task(bind=True)
def process_media_file_task(self, asset_id):
    #фоновая задача для celery для имитации долгой обработчки медиафайла
    try:
        #1 находим файл в бд
        asset = MediaAsset.objects.get(id=asset_id)
        asset.status = MediaAsset.Status.PROCESSING
        asset.save()

        #создаем лог задачи
        task_log = ProcessingTask.objects.create(
            asset=asset,
            step_name='async_pipeline_simulation',
            status='running',
            details='начало фоновой обработки файла..'
        )
        #имитируем тяжелную работу например конвертацию видео
        time.sleep(5)

        #2 обновление статуса на успешный
        asset.status = MediaAsset.Status.COMPLETED
        asset.save()

        task_log.status = 'success'
        task_log.details = 'Обработка успешно завершена воркером celery.'
        task_log.save()

        return f"asset {asset_id} processed sucessfully"

    except MediaAsset.DoesNotExist:
        return f"asset {asset_id} not found."
    except Exception as exc:
        #если произошла ошибка то фиксируем ее
        if 'asset' in locals():
            asset.status = MediaAsset.Status.FAILED
            asset.error_message = str(exc)
            asset.save()
        #перезапуск задачи при сбое (retry)
        raise self.retry(exc=exc, countdown=10, max_retries=3)
