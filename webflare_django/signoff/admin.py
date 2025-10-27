from django.contrib import admin
from .models import SignOff

from django.utils.html import format_html

@admin.register(SignOff)
class SignOffAdmin(admin.ModelAdmin):
    list_display = ('client', 'project', 'date', 'created_at', 'download_pdf')
    readonly_fields = ('created_at', 'pdf_preview')
    
    def download_pdf(self, obj):
        if obj.pdf_copy:
            return format_html('<a class="button" href="{}" download>Download PDF</a>', obj.pdf_copy.url)
        return "-"
    download_pdf.short_description = 'Signed Form'
    
    def pdf_preview(self, obj):
        if obj.pdf_copy:
            return format_html(
                '<div style="margin-top: 10px;">'
                '<h3>Signed Form Preview</h3>'
                '<iframe src="{}" width="100%" height="800px" style="border: 1px solid #ddd;"></iframe>'
                '<br><a class="button" href="{}" download style="margin-top: 10px;">Download PDF</a>'
                '</div>',
                obj.pdf_copy.url, obj.pdf_copy.url
            )
        return "No PDF available"
    pdf_preview.short_description = 'Signed Form Preview'
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client', 'project', 'date')
        }),
        ('Sign-off Status', {
            'fields': ('project_satisfaction', 'portfolio_permission', 'testimonial_opt_in')
        }),
        ('Testimonial', {
            'fields': ('rating', 'testimonial_text')
        }),
        ('Signature', {
            'fields': ('signer_name', 'signer_title', 'signer_date', 'signature_image')
        }),
        ('Document', {
            'fields': ('pdf_copy', 'pdf_preview', 'created_at')
        }),
    )
