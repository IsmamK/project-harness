from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import (
    ScraperService,
    distributed_parallel_scrape
)

class SearchView(APIView):
    def post(self, request):
        query = request.data.get('query', '').strip()
        if not query:
            return Response(
                {'error': 'Query is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Run all three methods
        results = {
            'linear': ScraperService.linear_scrape(query),
            'parallel': ScraperService.parallel_scrape(query),
            'distributed_parallel': distributed_parallel_scrape(query)
        }
        
        # Generate comparison metrics
        comparison = {
            'execution_times': {
                'linear': results['linear']['time_taken'],
                'parallel': results['parallel']['time_taken'],
                'distributed': results['distributed_parallel']['time_taken']
            },
            'resource_utilization': {
                'linear': results['linear']['processing_info'],
                'parallel': results['parallel']['processing_info'],
                'distributed': results['distributed_parallel']['processing_info']
            },
            'speedup_factors': {
                'parallel_vs_linear': results['linear']['time_taken'] / results['parallel']['time_taken'],
                'distributed_vs_linear': results['linear']['time_taken'] / results['distributed_parallel']['time_taken'],
                'distributed_vs_parallel': results['parallel']['time_taken'] / results['distributed_parallel']['time_taken']
            }
        }
        
        return Response({
            'query': query,
            'results': results,
            'comparison': comparison
        })