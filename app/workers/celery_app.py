from celery import Celery

celery_app = Celery("transaction_worker", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0", include=["app.workers.transaction_tasks"])