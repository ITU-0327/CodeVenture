from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
import requests
import time

SUCCESS = 3
WRONG_ANSWER = 4
RUN_TIME_ERROR = 11


def playground_view(request):
    return render(request, 'playground.html')


@csrf_exempt
def run_code(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        code = body_data.get('code', '')

        encoded_code = base64.b64encode(code.encode()).decode('utf-8')

        url = "https://judge0-ce.p.rapidapi.com/submissions/"

        querystring = {"base64_encoded": "true", "wait": "false", "fields": "*"}

        payload = {
            "language_id": 71,
            "source_code": encoded_code,
            "redirect_stderr_to_stdout": True
        }
        headers = {
            "content-type": "application/json",
            "Content-Type": "application/json",
            "X-RapidAPI-Key": "4488a01de2msh7b39afb80b4a53dp1f0172jsndd17e06649b3",
            "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
        }

        response = requests.post(url, json=payload, headers=headers, params=querystring)

        token = response.json().get('token')

        time.sleep(2)

        url = f"https://judge0-ce.p.rapidapi.com/submissions/{token}"

        querystring = {"base64_encoded": "true", "fields": "*"}

        headers = {
            "X-RapidAPI-Key": "4488a01de2msh7b39afb80b4a53dp1f0172jsndd17e06649b3",
            "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        response_data = response.json()
        status_id = response_data.get('status_id')

        max_retries = 10
        retry_count = 0

        while status_id != 3 and retry_count < max_retries:
            time.sleep(0.1)
            response = requests.get(url, headers=headers, params=querystring)
            response_data = response.json()
            status_id = response_data.get('status_id')
            retry_count += 1

        if status_id in [SUCCESS, WRONG_ANSWER, RUN_TIME_ERROR]:
            decoded_output = base64.b64decode(response_data.get('stdout', '')).decode('utf-8')
            return JsonResponse({'result': decoded_output})
        else:
            return JsonResponse({'error': 'Execution took too long or another error occurred.'})

    return JsonResponse({'error': 'Only POST method is supported.'})
