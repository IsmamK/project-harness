import os
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
from django.conf import settings
from time import time
from celery import shared_task
import socket
from itertools import chain
from celery.app.control import Inspect

class ScraperService:
    @staticmethod
    def google_search(query, num_results=10):
        """Fetch search results from Google Custom Search API"""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': settings.GOOGLE_API_KEY,
            'cx': settings.GOOGLE_CSE_ID,
            'q': query,
            'num': num_results
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return [item['link'] for item in data.get('items', [])]
        except Exception as e:
            print(f"Google search failed: {e}")
            return []

    @staticmethod
    def scrape_emails_from_url(url):
        """Scrape emails from a single URL"""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            
            return list(set(emails))
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            return []

    @staticmethod
    def linear_scrape(query):
        """Sequential scraping - baseline measurement"""
        start_time = time()
        urls = ScraperService.google_search(query)
        emails = []
        
        for url in urls:
            emails.extend(ScraperService.scrape_emails_from_url(url))
        
        return {
            'time_taken': time() - start_time,
            'pages_scraped': len(urls),
            'emails_found': emails,
            'processing_info': {
                'type': 'linear',
                'machines_used': 1,
                'threads_per_machine': 1,
                'total_threads': 1,
                'machine_details': [{
                    'hostname': socket.gethostname(),
                    'threads': 1,
                    'urls_processed': len(urls)
                }]
            }
        }

    @staticmethod
    def parallel_scrape(query, max_workers=5):
        """Single-machine parallel processing"""
        start_time = time()
        urls = ScraperService.google_search(query)
        emails = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(ScraperService.scrape_emails_from_url, urls)
            for result in results:
                emails.extend(result)
        
        return {
            'time_taken': time() - start_time,
            'pages_scraped': len(urls),
            'emails_found': emails,
            'processing_info': {
                'type': 'parallel',
                'machines_used': 1,
                'threads_per_machine': max_workers,
                'total_threads': max_workers,
                'machine_details': [{
                    'hostname': socket.gethostname(),
                    'threads': max_workers,
                    'urls_processed': len(urls)
                }]
            }
        }

    @staticmethod
    def distribute_urls(urls, batch_size=5):
        """Split URLs into batches for distribution"""
        return [urls[i:i + batch_size] for i in range(0, len(urls), batch_size)]

# services.py
from .tasks import process_url_batch


def distributed_parallel_scrape(query, threads_per_worker=4):
    """
    True distributed+parallel implementation
    """
    start_time = time()
    urls = ScraperService.google_search(query)
    url_batches = ScraperService.distribute_urls(urls)
    
    # Distribute batches to Celery workers
    tasks = [process_url_batch.delay(batch, threads_per_worker) for batch in url_batches]
    results = [task.get() for task in tasks]
    
    # Aggregate results
    all_emails = list(chain(*[res['emails'] for res in results]))
    machine_details = [res['processing_info'] for res in results]
    
    return {
        'time_taken': time() - start_time,
        'pages_scraped': len(urls),
        'emails_found': all_emails,
        'processing_info': {
            'type': 'distributed+parallel',
            'machines_used': len(machine_details),
            'threads_per_machine': threads_per_worker,
            'total_threads': len(machine_details) * threads_per_worker,
            'machine_details': machine_details
        }
    }