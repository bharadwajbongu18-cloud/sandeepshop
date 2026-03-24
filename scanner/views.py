from django.shortcuts import render
from django.http import HttpResponse
from openpyxl import Workbook
from urllib.parse import urlparse
from .models import Claim


# Home page
def home(request):
    return render(request, 'scan.html')


# 🔥 Correct QR Processing
def process_qr(request):
    url = request.POST.get('qr_data')

    if not url or "instagram.com" not in url:
        return render(request, 'result.html', {'error': 'Invalid QR'})

    # ✅ Correct username extraction (handles all cases)
    parsed = urlparse(url)
    path = parsed.path.strip('/')   # removes leading/trailing /
    
    if not path:
        return render(request, 'result.html', {'error': 'Invalid profile link'})

    username = path.split('/')[0]   # always gets correct username

    # 🔴 Check duplicate
    if Claim.objects.filter(username=username).exists():
        return render(request, 'result.html', {
            'status': 'exists',
            'username': username
        })

    # 🟢 Save new user
    Claim.objects.create(
        username=username,
        profile_link=url
    )

    return render(request, 'result.html', {
        'status': 'new',
        'username': username
    })


# 📥 Excel Export
def export_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Claims"

    # Header
    ws.append(["Username", "Profile Link", "Claimed At"])

    # Data
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