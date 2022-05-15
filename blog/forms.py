from django import forms
from .models import Comment, Contact


class CommentForm(forms.ModelForm):

    class Meta:
        name = 'نام شما'
        email = 'ایمیل'
        body = 'نظر خود را بنویسید...'
        name_label = 'نام'
        email_label = 'ایمیل'
        body_label = 'دیدگاه'

        model = Comment
        fields = ['name', 'email', 'body']
        widgets = {
            'name': forms.TextInput(attrs=
                                    {'class': 'form-control label-input100 input100',
                                     'placeholder': name}),

            'email': forms.EmailInput(attrs=
                                      {'class': 'form-control label-input100 input100',
                                       'placeholder': email}),

            'body': forms.Textarea(attrs=
                                   {'class': 'form-control label-input100 input100',
                                    'placeholder': body})

        }

        labels = {
            'name': name_label,
            'email': email_label,
            'body': body_label
        }

    def clean(self):
        error_message = 'قبلا این کامنت را فرستاده اید.'
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        body = self.cleaned_data['body']
        if Comment.objects.filter(name=name, email=email, body=body).exists():
            raise forms.ValidationError(error_message)


class ContactForm(forms.ModelForm):
    class Meta:
        first_name = 'نام...'
        last_name = 'نام خانوادگی...'
        message = 'پیام خود را بنویسید...'
        first_name_label = 'نام'
        last_name_label = 'نام خانوادگی'
        email_label = 'ایمیل'
        phone_label = 'شماره تلفن'
        message_label = 'پیام'

        model = Contact
        fields = ('first_name', 'last_name', 'email', 'phone', 'message')

        widgets = {
            'first_name': forms.TextInput(attrs=
                                          {'class': 'form-control label-input100 input100',
                                           'placeholder': first_name}),

            'last_name': forms.TextInput(attrs=
                                         {'class': 'form-control label-input100 wrap-input100 rs2-wrap-input100 '
                                                   'validate-input',
                                          'placeholder': last_name}),

            'email': forms.EmailInput(attrs=
                                      {'class': 'form-control label-input100 input100',
                                       'placeholder': 'exmp@gmail.com'}),

            'phone': forms.TextInput(attrs=
                                     {'class': 'form-control label-input100 input100',
                                      'placeholder': '9121231415'}),

            'message': forms.Textarea(attrs=
                                      {'class': 'form-control',
                                       'placeholder': message}),

        }
        labels = {
            'first_name': first_name_label,
            'last_name': last_name_label,
            'email': email_label,
            'phone': phone_label,
            'message': message_label,
        }
