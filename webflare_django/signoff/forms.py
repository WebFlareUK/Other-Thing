from django import forms
from django.core.exceptions import ValidationError
from .models import SignOff


class SignOffForm(forms.ModelForm):
    signature_data = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        project_satisfaction = cleaned_data.get('project_satisfaction')
        portfolio_permission = cleaned_data.get('portfolio_permission')
        
        if not project_satisfaction:
            raise ValidationError('You must confirm project satisfaction to proceed.')
        
        if not portfolio_permission:
            raise ValidationError('You must grant portfolio permission to proceed.')
        
        return cleaned_data

    class Meta:
        model = SignOff
        fields = [
            'provider', 'client', 'project', 'date',
            'project_satisfaction', 'portfolio_permission', 'testimonial_opt_in',
            'rating', 'testimonial_text',
            # Include the future-services interest checkboxes so they render in the form
            'interested_extra_pages', 'interested_gallery', 'interested_booking', 'interested_blog',
            'interested_email', 'interested_seo', 'interested_social', 'interested_ecommerce', 'interested_maintenance',
            'signer_name', 'signer_title', 'signer_date'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'testimonial_text': forms.Textarea(attrs={'rows': 6, 'class': 'testimonial-input form-input'}),
            'client': forms.TextInput(attrs={'class': 'form-input'}),
            'interested_extra_pages': forms.CheckboxInput(attrs={'class': 'service-checkbox'}),
            'interested_gallery': forms.CheckboxInput(attrs={'class': 'service-checkbox'}),
            'interested_booking': forms.CheckboxInput(attrs={'class': 'service-checkbox'}),
            'interested_blog': forms.CheckboxInput(attrs={'class': 'service-checkbox'}),
            'interested_email': forms.CheckboxInput(attrs={'class': 'service-checkbox'}),
            'interested_seo': forms.CheckboxInput(attrs={'class': 'service-checkbox'}),
            'interested_social': forms.CheckboxInput(attrs={'class': 'service-checkbox'}),
            'interested_ecommerce': forms.CheckboxInput(attrs={'class': 'service-checkbox'}),
            'interested_maintenance': forms.CheckboxInput(attrs={'class': 'service-checkbox'}),
            'project': forms.TextInput(attrs={'class': 'form-input'}),
            'provider': forms.TextInput(attrs={'class': 'form-input'}),
            'signer_name': forms.TextInput(attrs={'class': 'form-input'}),
            'signer_title': forms.TextInput(attrs={'class': 'form-input'}),
            'signer_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'project_satisfaction': forms.CheckboxInput(attrs={'class': 'checkbox-input'}),
            'portfolio_permission': forms.CheckboxInput(attrs={'class': 'checkbox-input'}),
            'testimonial_opt_in': forms.CheckboxInput(attrs={'class': 'checkbox-input'}),
        }
