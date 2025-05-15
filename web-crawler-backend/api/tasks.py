# api/tasks.py

from celery import shared_task
from concurrent.futures import ThreadPoolExecutor
from .services import ScraperService
import socket

@shared_task(bind=True)
def process_url_batch(self, url_batch, threads_per_worker=4):
    emails = []
    with ThreadPoolExecutor(max_workers=threads_per_worker) as executor:
        results = list(executor.map(ScraperService.scrape_emails_from_url, url_batch))
        for result in results:
            emails.extend(result)
    
    return {
        'emails': emails,
        'processing_info': {
            'hostname': socket.gethostname(),
            'threads_used': threads_per_worker,
            'urls_processed': len(url_batch)
        }
    }
