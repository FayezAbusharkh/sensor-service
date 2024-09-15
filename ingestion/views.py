import csv
import io
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SensorData
import numpy as np
import json

@api_view(['POST'])
def ingest_csv(request):
    url = request.query_params.get('url')
    if not url:
        return Response({"error": "No URL provided"}, status=400)

    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
    except requests.RequestException as e:
        return Response({"error": str(e)}, status=400)

    try:
        csv_file = io.StringIO(response.content.decode('utf-8'))
        reader = csv.DictReader(csv_file)
    except Exception as e:
        return Response({"error": "Failed to read CSV: " + str(e)}, status=400)

    data = []

    for row in reader:
        data.append(SensorData(
            id=row['id'],
            type=row['type'],
            subtype=row['subtype'],
            reading=row['reading'],
            location=row['location'],
            timestamp=row['timestamp']
        ))

    SensorData.objects.bulk_create(data)

    return Response({"message": f"CSV data ingested successfully"}, status=201)


@api_view(['GET'])
def get_median(request):
    filter_params = request.query_params.get('filter', None)
    
    queryset = SensorData.objects.all()

    if filter_params:
        try:
            filter_json = json.loads(filter_params)
            
            if 'id' in filter_json:
                queryset = queryset.filter(id__in=filter_json['id'])
            if 'type' in filter_json:
                queryset = queryset.filter(type__in=filter_json['type'])
            if 'subtype' in filter_json:
                queryset = queryset.filter(subtype__in=filter_json['subtype'])
            if 'location' in filter_json:
                queryset = queryset.filter(location__in=filter_json['location'])
                
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format in filter"}, status=400)

    readings = list(queryset.values_list('reading', flat=True))

    if not readings:
        return Response({"error": "No data available for the given filters"}, status=404)

    median_value = np.median(readings)

    return Response({
        "count": len(readings),
        "median": median_value
    }, status=200)