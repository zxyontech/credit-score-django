import os
import pickle
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = pickle.load(open(os.path.join(BASE_DIR, 'rf_model.pkl'), 'rb'))
scaler = pickle.load(open(os.path.join(BASE_DIR, 'scaler.pkl'), 'rb'))

def index(request):
    return render(request, 'predictor/index.html')

def predict(request):
    if request.method == 'POST':
        try:
            features = [
                float(request.POST.get('outstanding_debt')),
                float(request.POST.get('interest_rate')),
                float(request.POST.get('delay_from_due_date')),
                float(request.POST.get('changed_credit_limit')),
                float(request.POST.get('credit_mix')),
                float(request.POST.get('num_credit_inquiries')),
                float(request.POST.get('num_credit_card')),
                float(request.POST.get('annual_income')),
                float(request.POST.get('total_emi_per_month')),
                float(request.POST.get('credit_utilization_ratio')),
            ]
            scaled = scaler.transform([features])
            result = model.predict(scaled)[0]

            color = {'Good': 'green', 'Standard': 'orange', 'Poor': 'red'}
            emoji = {'Good': '✅', 'Standard': '⚠️', 'Poor': '❌'}

            return render(request, 'predictor/index.html', {
                'result': result,
                'color': color.get(result, 'gray'),
                'emoji': emoji.get(result, ''),
            })
        except Exception as e:
            return render(request, 'predictor/index.html', {'error': str(e)})
    return render(request, 'predictor/index.html')