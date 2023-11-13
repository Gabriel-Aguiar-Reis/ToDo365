from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Tarefa(models.Model):
    """
    Modelo para representar uma tarefa.
    """

    titulo = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    data_horario = models.DateTimeField()
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tarefas',
        on_delete=models.CASCADE,
        blank=True,
    )

    def __str__(self):
        """
        Retorna a representação em string da tarefa.
        """
        return f'{self.titulo} <{self.usuario}>'


class Usuario(AbstractUser):
    """
    Modelo para representar um usuário costumizado com campos adicionais.
    """

    class Meta:
        db_table = 'auth_user'

    email = models.EmailField(blank=False)
    validado = models.BooleanField(default=False)

    def __str__(self):
        """
        Retorna a representação em string do usuário.
        """
        return self.get_full_name()
