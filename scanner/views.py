from django.shortcuts import render
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Claim

def home(request):
    return render(request, 'scan.html')


def process_qr(request):
    url = request.POST.get('qr_data')

    if not url or "instagram.com" not in url:
        return render(request, 'result.html', {'error': 'Invalid QR'})

    username = url.strip('/').split('/')[-1]

    if Claim.objects.filter(username=username).exists():
        return render(request, 'result.html', {
            'status': 'exists',
            'username': username
        })

    Claim.objects.create(username=username, profile_link=url)

    return render(request, 'result.html', {
        'status': 'new',
        'username': username
    })


def export_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Claims"

    ws.append(["Username", "Profile Link", "Claimed At"])

    for claim in Claim.objects.all():
        ws.append([
            claim.username,
            claim.profile_link,
            str(claim.claimed_at)
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=claims.xlsx'

    wb.save(response)
    return response