from django import forms
from accounts.models import User

class SignUpForm(forms.ModelForm):

        
    username = forms.CharField(label="名前")
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password',]

    def save(self):
        user = super().save(commit=False)
        #validate_password(self.cleaned_data.get('password'), user)
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        return user    