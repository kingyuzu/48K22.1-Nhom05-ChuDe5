from django import forms
from admin_manager.models import Order, Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'subject', 'priority', 'status']
    
    OrderID = forms.ModelChoiceField(queryset=Order.objects.all(), required=False, empty_label="None")  # Make this optional
    Status = forms.ChoiceField(choices=Ticket.TicketStatus, required=False)

    # Customizing the form field appearance (optional)
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)

        # Add Bootstrap styling for form fields
        self.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ticket title'})
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the issue', 'rows': 4})
        self.fields['subject'].widget = forms.Select(choices=Ticket.SubjectChoices, attrs={'class': 'form-control'})
        self.fields['priority'].widget = forms.Select(choices=Ticket.PriorityChoices, attrs={'class': 'form-control'})
        self.fields['order'].widget = forms.Select(attrs={'class': 'form-control'})

        # Set the default value for Status field to 'New' and hide it
        self.fields['status'].initial = Ticket.TicketStatus.NEW  # Default value
        self.fields['status'].widget = forms.HiddenInput()

        # Optionally, hide the User field
        if 'user' in self.fields:
            self.fields['user'].widget = forms.HiddenInput()
