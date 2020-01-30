from django import forms


class ContactForm(forms.Form):
    from_email = forms.EmailField(label='Adresse e-mail',required=True)
    subject = forms.CharField(label='Sujet', required=True)
    message = forms.CharField(label='Message', widget=forms.Textarea, required=True)