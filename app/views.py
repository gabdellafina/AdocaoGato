import base64
from datetime import timedelta
import io
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
import urllib
from app.forms import formCadastro, formCadastroGato, formFoto, formLogin
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from app.models import Foto, Gato, Usuario, Adocoes
from django.contrib.auth import get_user_model,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.template import loader
import matplotlib.pyplot as plt
from django.utils.timezone import now


# Create your views here.

def home(request):
    return render(request,"home.html")

def cadastro(request):
    novo_user = formCadastro(request.POST, request.FILES)

    if request.method == 'POST':
        email = request.POST.get('email')
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "E-mail já cadastrado.")
        elif novo_user.is_valid():
            user = novo_user.save(commit=False)
            user.senha = make_password(novo_user.cleaned_data['senha'])
            user.save()
            messages.success(request, "Usuário cadastrado com sucesso")
            return redirect('home')
    
    context = {'form': novo_user}
    return render(request, "cadastro.html", context)

def login(request):
   form_login = formLogin(request.POST or None)
   if request.POST:
      _email = request.POST['email']
      _senha = request.POST['senha']
      
      try:
         usuario = Usuario.objects.get(email = _email)      
         if check_password(_senha,usuario.senha):
            request.session.set_expiry(timedelta(seconds=1800))
            request.session['email'] = _email
            messages.success(request,"Usuario logado com sucesso")
            return redirect('dashboard')
         else:
            messages.error("Senha incorreta")
      except:
            messages.error(request, 'Usuario não encontrado!')
            return redirect('login')
            
   context = {
      'form' : form_login
   }
   return render(request,'login.html',context)

def dashboard(request):
    if 'email' not in request.session:
        return redirect('login')

    # Obtém o usuário logado
    usuario_logado = Usuario.objects.get(email=request.session['email'])

    context = {
        'usuario': usuario_logado,
        'email': request.session['email'],
    }

    template = loader.get_template("dashboard.html")
    return HttpResponse(template.render(context))


def cadastroGato(request):
    if request.method == 'POST':
        form = formCadastroGato(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            messages.success(request, "Gato cadastrado com sucesso!")
            return redirect('home') 
    else:
        form = formCadastroGato() 

    return render(request, 'cadastroGato.html', {'form': form})

def gatos(request):
   gatos = Gato.objects.all().values()

   context = {
      'dados' : gatos
   }
   return render(request,'gatos.html',context)

def criar_foto(request):
    if request.method == 'POST':
        form = formFoto(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('galeria')
    else:
        form = formFoto()

    return render(request, 'criar_foto.html', {'form': form})

def usuarios(request):
   usuarios = Usuario.objects.all().values()

   context = {
      'dados' : usuarios
   }
   return render(request,'usuarios.html',context)

def pagina_sucesso(request):
   return render(request,'pagina_sucesso.html')


def editar_usuario(request,id_usuario):
   usuario = Usuario.objects.get(id=id_usuario)
   form = formCadastro(request.POST or None,instance=usuario)
   if request.POST:
      if form.is_valid():
         form.save()
         return redirect('exibir_usuario')
   context = {
      'form' : form
   }

   return render(request,'editar_usuario.html',context)

def excluir_usuario(request,id_usuario):
   usuario = Usuario.objects.get(id=id_usuario)
   usuario.delete()
   return redirect('exibir_usuario')

def mostrar_fotos(request):
    fotos = Foto.objects.all()

    context = {
        'dados': fotos  
        }

    return render(request, "galeria.html", context)

def exibir_usuario(request):
   usuarios = Usuario.objects.all().values()

   context = {
      'dados' : usuarios
   }
   return render(request,'usuarios.html',context)

def grafico(request):
    gatos = Gato.objects.all().values()
    nomes = [gato['nome'] for gato in gatos]
    idades = [gato['idade'] for gato in gatos]

    fig, xy = plt.subplots()
    xy.bar(nomes,idades)
    xy.set_xlabel('Nomes dos gatos')
    xy.set_ylabel('Idades dos gatos')
    xy.set_title('Gatos')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    context = {
        'data' : uri
    }

    return render(request,'grafico.html',context)

def adocao(request, gato_id):
    User = get_user_model()
    usuario = request.user

    gato = get_object_or_404(Gato, id=gato_id)

    if request.method == 'POST':
        adocao = Adocoes(usuario=usuario, gato=gato)
        adocao.save()
        
        messages.success(request, f"Parabéns! Você adotou o gato {gato.nome}.")
        return redirect('gatos_disponiveis')

    context = {
        'gato': gato,
    }
    return render(request, 'adocao.html', context)

def gatos_disponiveis(request):
    gatos_disponiveis = Gato.objects.exclude(id__in=Adocoes.objects.values('gato'))
    quantidade_gatos = gatos_disponiveis.count()

    context = {
        'gatos': gatos_disponiveis,
        'quantidade': quantidade_gatos,
    }
    return render(request, 'gatos.html', context)
