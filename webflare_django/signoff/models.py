from django.db import models
from django.utils import timezone


class SignOff(models.Model):
    provider = models.CharField(max_length=255, default='WebFlare')
    client = models.CharField(max_length=255)
    project = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)

    # Checkboxes
    project_satisfaction = models.BooleanField(
        default=False,
        help_text="Confirmation that all services have been completed satisfactorily"
    )
    portfolio_permission = models.BooleanField(
        default=False,
        help_text="Permission to use the project in portfolio and marketing materials"
    )
    testimonial_opt_in = models.BooleanField(
        default=False,
        help_text="Optional: Provide a testimonial for our services"
    )

    # Testimonial
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    testimonial_text = models.TextField(blank=True)

    # Signer
    signer_name = models.CharField(max_length=255, blank=True)
    signer_title = models.CharField(max_length=255, blank=True)
    signer_date = models.DateField(null=True, blank=True)

    # Future Services Interest
    interested_extra_pages = models.BooleanField(default=False, verbose_name="Extra pages")
    interested_gallery = models.BooleanField(default=False, verbose_name="Gallery/Portfolio page")
    interested_booking = models.BooleanField(default=False, verbose_name="Booking system")
    interested_blog = models.BooleanField(default=False, verbose_name="Blog/News section")
    interested_email = models.BooleanField(default=False, verbose_name="Email setup")
    interested_seo = models.BooleanField(default=False, verbose_name="SEO setup")
    interested_social = models.BooleanField(default=False, verbose_name="Social feed integration")
    interested_ecommerce = models.BooleanField(default=False, verbose_name="E-commerce setup")
    interested_maintenance = models.BooleanField(default=False, verbose_name="Hosting & maintenance")

    # Future Services Prices
    extra_pages_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Extra pages price")
    gallery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Gallery/Portfolio price")
    booking_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Booking system price")
    blog_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Blog/News price")
    email_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Email setup price")
    seo_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="SEO setup price")
    social_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Social feed price")
    ecommerce_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="E-commerce price")
    maintenance_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Hosting & maintenance price")

    # Signature image
    signature_image = models.ImageField(upload_to='signatures/', null=True, blank=True)

    # PDF copy of the completed form
    pdf_copy = models.FileField(upload_to='signed_forms/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SignOff: {self.client} - {self.project} ({self.date})"
