import json
from django.shortcuts import render
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from pathlib import Path
from decimal import Decimal
cur_dir=Path.cwd()
import pandas as pd
# Create your views here.



class filter_waist_measurements(APIView):
    def post(self,request):
        if request.method == 'POST':
            try:
                # height, weight, and age from request data
                height = float(request.data['height'])
                weight = float(request.data['weight'])
                age = float(request.data['age'])  
                print(height,weight,age)

                # read CSV file data
                with open(str(cur_dir)+'\measurements.csv', 'r') as file:
                    reader = csv.DictReader(file)
                    data = list(reader)

                    # filter the data based on height, weight, and age
                    filtered_data = [d for d in data if float(d.get('Age')) == age and float(d.get('Height(cm)')) == height and float(d.get('Weight(kgs)')) == weight]

                    waist_measurements = sorted(list(set([d['Waist(cm)'] for d in filtered_data])))
                    waist_measurements.append("other")
       
                    return JsonResponse({'data': waist_measurements})
                
            except Exception as e:
                return JsonResponse({'error': 'Missing Some Parameters: {}'.format(e)})
        else:
            return JsonResponse({'error': 'POST request required'})
            
class add_waist_measurements(APIView):
    def post(self,request):
        if request.method == 'POST':
            try:
                # height, weight, age, and waist from request data
                height = float(request.data['height'])
                weight = float(request.data['weight'])
                age = float(request.data['age'])  
                waist = float(request.data['waist'])
            
                # read CSV file data
                with open(str(cur_dir)+'\measurements.csv', 'r') as file:
                    reader = csv.DictReader(file)
                    data = list(reader)
            
                    # filter the data based on height, weight, age and waist      
                    filtered_data = [d for d in data if float(d.get('Age')) == age and float(d.get('Height(cm)')) == height and float(d.get('Weight(kgs)')) == weight and Decimal(d.get('Waist(cm)')).quantize(Decimal('0.01')) == Decimal(waist).quantize(Decimal('0.01'))]
                    if filtered_data:
                        waist_measurements = sorted(list(set([d['Waist(cm)'] for d in filtered_data])))
                        waist_measurements.append("other")
                        return JsonResponse({"msg":"Measurement data already exists", 'waist_measurements': waist_measurements})
                    else:
                        # if the measurement does not exist, add it to the measurements CSV file
                        with open(str(cur_dir)+'\measurements.csv', 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([height, weight, age, waist])
                            return JsonResponse({"msg":'Measurement added'}, safe=False)
            except Exception as e:
                    return JsonResponse({'error': 'Missing Some Parameters: {}'.format(e)})
        else:
            return JsonResponse({'error': 'POST request required'})

