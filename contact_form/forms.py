
from django import forms
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.template import loader
from django.utils.translation import ugettext_lazy as _


class BaseEmailFormMixin(object):
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email for _, email in settings.MANAGERS]

    subject_template_name = 'contact_form/email_subject.txt'
    message_template_name = 'contact_form/email_template.txt'

    def get_message(self):
        return loader.render_to_string(self.message_template_name, self.get_context())

    def get_subject(self):
        subject = loader.render_to_string(self.subject_template_name, self.get_context())
        return ''.join(subject.splitlines())

    def get_context(self):
        if not self.is_valid():
            raise ValueError("Cannot generate Context when form is invalid.")
        return self.cleaned_data

    def get_message_dict(self):
        return {
            "from_email": self.from_email,
            "to": self.recipient_list,
            "subject": self.get_subject(),
            "body": self.get_message(),
        }

    def send_email(self, request, fail_silently=False):
        self.request = request
        EmailMessage(**self.get_message_dict()).send(fail_silently=fail_silently)


class ContactForm(forms.Form, BaseEmailFormMixin):
    """
    Subclass this and declare your own fields.
    """


class ContactModelForm(forms.ModelForm, BaseEmailFormMixin):
    """
    You'll need to declare the model yourself.
    """


class BasicContactForm(ContactForm):
    """
    A very basic contact form you can use out of the box if you wish.
    """
    name = forms.CharField(label=_(u'Name'), max_length=100)
    email = forms.EmailField(label=_(u'Email'), max_length=200)
    body = forms.CharField(label=_(u'Body'), widget=forms.Textarea())
