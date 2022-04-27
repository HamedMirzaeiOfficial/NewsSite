from django import forms
from .models import Comment, Contact


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        widgets = {
            'name': forms.TextInput(attrs=
                                    {'class': 'form-control label-input100 input100',
                                     'placeholder': 'نام شما'}),

            'email': forms.EmailInput(attrs=
                                      {'class': 'form-control label-input100 input100',
                                       'placeholder': 'ایمیل'}),

            'body': forms.Textarea(attrs=
                                   {'class': 'form-control label-input100 input100',
                                    'placeholder': 'نظر خود را بنویسید...'})

        }

        labels = {
            'name': 'نام',
            'email': 'ایمیل',
            'body': 'دیدگاه'
        }

    def clean(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        body = self.cleaned_data['body']
        if Comment.objects.filter(name=name, email=email, body=body).exists():
            raise forms.ValidationError('قبلا این کامنت را فرستاده اید.')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'phone', 'message')

        widgets = {
            'first_name': forms.TextInput(attrs=
                                          {'class': 'form-control label-input100 input100',
                                           'placeholder': 'نام...'}),

            'last_name': forms.TextInput(attrs=
                                         {'class': 'form-control label-input100 wrap-input100 rs2-wrap-input100 '
                                                   'validate-input',
                                          'placeholder': 'نام خانوادگی...'}),

            'email': forms.EmailInput(attrs=
                                      {'class': 'form-control label-input100 input100',
                                       'placeholder': 'exmp@gmail.com'}),

            'phone': forms.TextInput(attrs=
                                     {'class': 'form-control label-input100 input100',
                                      'placeholder': '9121231415'}),

            'message': forms.Textarea(attrs=
                                      {'class': 'form-control',
                                       'placeholder': 'پیام خود را بنویسید...'}),

        }
        labels = {
            'first_name': 'نام*',
            'last_name': 'نام خانوادگی*',
            'email': 'ایمیل*',
            'phone': 'شماره تلفن*',
            'message': 'پیام',
        }
