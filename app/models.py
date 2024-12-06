from django.db import models
import uuid


def rename_image(instance, filename):
    ext = filename.split('.')[-1]
    return f'imagens/courses/{uuid.uuid4()}.{ext}'

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to='imagens/users/', null=True)

class Foto(models.Model):
    titulo = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='imagens/', null=True)


class Gato(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    raca = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='imagens/gatos/', null=True)

class Adocoes(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    gato = models.ForeignKey(Gato, on_delete=models.CASCADE)
    data_adocao = models.DateField(auto_now_add=True)
