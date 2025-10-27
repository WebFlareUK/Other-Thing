import base64
import os
from io import BytesIO
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from PIL import Image, UnidentifiedImageError
import weasyprint
from .forms import SignOffForm


def signoff_view(request):
    if request.method == 'POST':
        form = SignOffForm(request.POST)
        if form.is_valid():
            signoff = form.save(commit=False)
            # Handle signature data (a data URL)
            signature_data = form.cleaned_data.get('signature_data')
            if signature_data:
                # expected format: data:image/png;base64,....
                header, b64data = signature_data.split(',', 1)
                try:
                    decoded = base64.b64decode(b64data)
                    # attempt to detect image type using Pillow
                    ext = 'png'
                    try:
                        img = Image.open(BytesIO(decoded))
                        fmt = (img.format or '').lower()
                        if fmt:
                            ext = 'jpg' if fmt == 'jpeg' else fmt
                    except UnidentifiedImageError:
                        ext = 'png'

                    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
                    safe_client = ''.join(c if c.isalnum() else '_' for c in (signoff.client or 'client'))
                    filename = f"signature_{safe_client}_{timestamp}.{ext}"
                    # Save to model ImageField
                    signoff.signature_image.save(filename, ContentFile(decoded), save=False)
                except Exception:
                    # If decoding fails, ignore signature (could add logging)
                    pass

            # Save the model first to ensure all related files are stored
            signoff.save()
            
            # Get paths for static files
            import os
            from django.conf import settings
            logo_path = os.path.join(settings.BASE_DIR, 'signoff', 'static', 'signoff', 'WebFlare-Logo.png')
            signature_path = signoff.signature_image.path if signoff.signature_image else None
            
            # Generate PDF using the PDF-specific template
            html = render_to_string('signoff/form_pdf.html', {
                'signoff': signoff,
                'logo_path': logo_path,
                'signature_path': signature_path,
            })
            
            # Configure WeasyPrint with styles
            css = weasyprint.CSS(string="""
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
                @page {
                    margin: 0;
                    size: A4;
                }
                body {
                    margin: 0;
                    padding: 36px;
                    font-family: 'Inter', sans-serif;
                    color: #0f172a;
                    background: #ffffff;
                }
                .container {
                    max-width: 980px;
                    margin: 0 auto;
                    background: #ffffff;
                }
                .header {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 28px 36px;
                    border-bottom: 1px solid #e6eef8;
                    background: linear-gradient(180deg,#ffffff,#fbfdff);
                }
                .logo { height: 56px; }
                .doc-title h1 {
                    margin: 0;
                    font-size: 20px;
                    font-weight: 700;
                    color: #0f172a;
                }
                .content { padding: 28px 36px; }
                .project-info {
                    background: #f8fbff;
                    padding: 18px;
                    border: 1px solid #e6eef8;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }
                .info-grid {
                    display: grid;
                    grid-template-columns: 160px 1fr;
                    gap: 10px 20px;
                    align-items: center;
                }
                .info-label {
                    font-weight: 700;
                    color: #64748b;
                }
                h2 {
                    margin-top: 28px;
                    margin-bottom: 12px;
                    font-size: 18px;
                    border-bottom: 2px solid #eef4ff;
                    padding-bottom: 10px;
                }
                h3 {
                    margin-top: 20px;
                    margin-bottom: 10px;
                    font-size: 16px;
                }
                .intro-text {
                    color: #64748b;
                    line-height: 1.6;
                }
                .service-card {
                    padding: 14px 0 14px 24px;
                    border-bottom: 1px solid #f1f6fb;
                    position: relative;
                }
                .service-card:last-child { border-bottom: none; }
                .service-card h4 {
                    margin: 0 0 8px 0;
                    font-size: 15px;
                    font-weight: 600;
                    color: #0f172a;
                }
                .service-card p {
                    margin: 0;
                    color: #64748b;
                    font-size: 14px;
                    line-height: 1.5;
                }
                .service-card::before {
                    content: "";
                    display: block;
                    position: absolute;
                    left: 8px;
                    top: 19px;
                    width: 4px;
                    height: 4px;
                    border-radius: 50%;
                    background-color: #2563eb;
                    opacity: 0.6;
                }
                .checkbox-item {
                    position: relative;
                    background: #fff;
                    border: 1px solid #e6eef8;
                    padding: 16px;
                    border-radius: 10px;
                    margin: 14px 0;
                }
                .checkbox-header {
                    display: flex;
                    gap: 14px;
                }
                .checkbox {
                    width: 22px;
                    height: 22px;
                    border-radius: 6px;
                    border: 2px solid #c7d2fe;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: #fff;
                    flex-shrink: 0;
                }
                .checkbox-item.checked .checkbox {
                    background: #2563eb;
                    border-color: #2563eb;
                }
                .checkbox .checkmark {
                    color: #fff;
                    font-weight: 700;
                }
                .checkbox-title {
                    font-weight: 700;
                    margin-bottom: 6px;
                }
                .checkbox-text {
                    color: #64748b;
                    font-size: 14px;
                }
                .testimonial-container {
                    margin-top: 12px;
                    padding: 14px;
                    background: #f8fbff;
                    border: 1px solid #e6eef8;
                    border-radius: 8px;
                }
                .star-rating {
                    color: #f59e0b;
                    font-size: 24px;
                    margin-bottom: 12px;
                }
                .signature-section {
                    margin-top: 28px;
                    padding: 20px;
                    background: #fff;
                    border: 1px solid #f1f6fb;
                    border-radius: 10px;
                }
                .signature-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 16px;
                }
                .signature-field label {
                    display: block;
                    margin-bottom: 8px;
                    font-weight: 600;
                }
                .signature-image {
                    max-width: 300px;
                    margin-top: 10px;
                }
            """)
            
            # Generate PDF with styles
            pdf_file = weasyprint.HTML(
                string=html,
                base_url=settings.BASE_DIR
            ).write_pdf(stylesheets=[css])
            
            # Debug information
            print("Generating PDF with:")
            print(f"- Logo path: {logo_path}")
            print(f"- Signature path: {signature_path}")
            print(f"- Base URL: {settings.BASE_DIR}")
            
            # Save PDF
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            safe_client = ''.join(c if c.isalnum() else '_' for c in (signoff.client or 'client'))
            filename = f"signoff_{safe_client}_{timestamp}.pdf"
            signoff.pdf_copy.save(filename, ContentFile(pdf_file), save=True)
            
            return redirect(reverse('signoff:thanks'))
    else:
        form = SignOffForm(initial={'client': 'Safe Let Property Management LTD', 'project': 'Squarespace Website Development'})

    return render(request, 'signoff/form.html', {'form': form})


def thanks_view(request):
    # Get the most recent signoff for this session
    from .models import SignOff
    signoff = SignOff.objects.order_by('-created_at').first()
    return render(request, 'signoff/thanks.html', {'signoff': signoff})
