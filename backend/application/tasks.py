from celery import shared_task
from .models import ServiceRequest, User
from .utils import format_report
from .mail import send_email
from datetime import datetime
# import time
import csv
import requests

@shared_task(ignore_result = False, name = 'download_csv_report')
def csv_report():
    service_requests = ServiceRequest.query.all()
    csv_filename = f"service_requests_{datetime.now().strftime('%f')}.csv" #service_requests_12345.csv
    with open(f'static/{csv_filename}', 'w', newline="") as csvfile:
        sr_no = 1
        service_requests_csv = csv.writer(csvfile, delimiter = ',')
        service_requests_csv.writerow(['Sr No', 'Service Request ID', 'Service ID', 'Customer ID', 'Professional ID', 'Address', 'Date of Request', 'Date of Completion', 'Status', 'Remarks', 'Customer Contact Number'])
        for service_request in service_requests:
            service_requests_csv.writerow([sr_no, service_request.id, service_request.service_id, service_request.customer_id, service_request.professional_id, service_request.address, service_request.date_of_request, service_request.date_of_completion, service_request.status, service_request.remarks, service_request.customer_contact_number])
            sr_no += 1
    
    return csv_filename


@shared_task(ignore_result = False, name = 'monthly_report')
def monthly_report():
    users = User.query.all()
    for user in users[1:]:
        user_data = {}
        user_data["name"] = user.name
        user_data["email"] = user.email
        user_service_requests = []
        service_requests = []
        if "customer" in user.roles:
            service_requests = ServiceRequest.query.filter_by(customer_id = user.id).all()
        elif "professional" in user.roles:
            service_requests = ServiceRequest.query.filter_by(professional_id = user.id).all()
        for service_request in service_requests:
            user_service_requests.append({
                "service_request_id": service_request.id,
                "service_id": service_request.service_id,
                "customer_id": service_request.customer_id,
                "professional_id": service_request.professional_id,
                "date_of_request": service_request.date_of_request,
                "date_of_completion": service_request.date_of_completion,
                "status": service_request.status,
                "remarks": service_request.remarks,
                "customer_contact_number": service_request.customer_contact_number,
            })
        user_data["service_requests"] = user_service_requests
        message = format_report("templates/mail_details.html", data = user_data)
        send_email(user.email, subject = "Monthly Service Requests Report - FixItFixIt", message = message)
    return "Monthly reports sent"

@shared_task(ignore_result = False, name = 'service_request_notification')
def service_request_notification(username, status):
    text = f"Hi {username}, your service request has been {status}."
    response = requests.post("https://chat.googleapis.com/v1/spaces/AAAAvzABVXs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=I4isTZV-pxGA918MVmMdqerdpg_2fbM7QwVLhIcbrSM", json = {"text": text})
    return "Service request notification sent"

@shared_task(ignore_result = False, name = 'service_requests_reminder')
def service_requests_reminder():
    users = User.query.all()
    for user in users:
        if "professional" in user.roles:
            service_requests = ServiceRequest.query.filter_by(professional_id=user.id, status='requested').all()
            if len(service_requests) > 0:
                text = f"Hi {user.name}, you have {len(service_requests)} service requests pending. Please visit the website to take action."
                response = requests.post("https://chat.googleapis.com/v1/spaces/AAAAvzABVXs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=I4isTZV-pxGA918MVmMdqerdpg_2fbM7QwVLhIcbrSM", json = {"text": text})
    
    return "Service requests reminder sent"
