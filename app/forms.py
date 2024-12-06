from django import forms

from app.models import Foto, Gato, Usuario


class formCadastro(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome', 'email', 'senha','imagem') 

    def clean(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.validationError("Email ja existente.")
        return email    
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'email': forms.EmailInput(attrs={'placeholder': 'usuario@email.com', 'class': 'form-control form-control-lg'}),
            'senha': forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
            'imagem': forms.FileInput(attrs={'accept': 'image/*'})
        }

class formLogin(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('email','senha')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'usuario@email.com', 'class': 'form-control form-control-lg'}),
            'senha': forms.PasswordInput(attrs={'class': 'form-control form-control-lg'})
        }

class formCadastroGato(forms.ModelForm):
    class Meta:
        model = Gato
        fields = ('nome','raca','idade','imagem')
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'raca': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'idade': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'imagem': forms.FileInput(attrs={'accept': 'image/*'})
    }
        
class formFoto(forms.ModelForm):
    class Meta:
        model = Foto
        fields = ['titulo', 'imagem']

        widgets = {
                'imagem': forms.FileInput(attrs={'accept': 'image/*'})
                }
        