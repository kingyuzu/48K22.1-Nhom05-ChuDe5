from django import forms
from admin_manager.models import Campaign


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['mail_subject', 'mail_content']
