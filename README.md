# HARNESS

**High-performance Asynchronous Retrieval and Navigation for Email & Site Scraping**

---

## About HARNESS

HARNESS is a distributed, scalable email scraping system designed to extract email addresses from web pages efficiently at scale. It leverages multiple scraping approaches—including linear, parallel, and distributed methods—to optimize performance and resource utilization.

Using the Google Custom Search API to identify relevant web pages, HARNESS applies advanced email extraction techniques combining regex, NLP, and DOM analysis for high precision. The system supports auto-scaling of distributed Celery workers managed by Kubernetes, providing robust and fault-tolerant scraping capabilities.

---

## Key Features

- **Google Custom Search API Integration:** Find relevant web pages efficiently.
- **Email Extraction:** Accurate harvesting with BeautifulSoup and regex patterns.
- **Parallel Processing:** Multithreaded scraping on single machines.
- **Distributed Workers:** Celery workers distributed across multiple nodes.
- **Auto-scaling Infrastructure:** Dynamic worker scaling with Kubernetes orchestration.
- **Containerized Deployment:** Dockerized services for easy deployment and management.
- **User-friendly Web GUI:** Built with Next.js and Tailwind CSS for interactive job submission and real-time results.

---

## Architecture Overview

- **Frontend:** Next.js React application with Tailwind CSS for styling.
- **Backend:** Django REST API managing scraping tasks and orchestration.
- **Task Queue:** Celery with Redis as the message broker for distributed task processing.
- **Scraping Engines:** Multiple scraping approaches (linear, parallel, distributed).
- **Deployment:** Docker containers orchestrated via Kubernetes for scalability and reliability.

---

## Getting Started

### Prerequisites

- Docker
- Kubernetes cluster or local minikube
- Python 3.10+
- Node.js 16+

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/HARNESS.git
   cd HARNESS
   ```
