from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from .models import Tarefa


class TarefaSerializer(serializers.ModelSerializer):
    """
    Serializador para a classe Tarefa.
    """

    class Meta:
        model = Tarefa
        fields = '__all__'

    def validate_data_horario(self, value):
        """
        Validação personalizada para o campo data_horario.
        """
        if value < timezone.now():
            raise serializers.ValidationError('Data ou Horário inválidos.')
        return value


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para a classe Usuario.
    """

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'password',
            'email',
            'tarefas',
            'validado',
            'is_superuser',
        ]

    def create(self, validated_data):
        """
        Criação correta de um novo usuário encriptando senha na serialização.
        """
        validated_data['password'] = make_password(validated_data['password'])
        return super(UsuarioSerializer, self).create(validated_data)

    tarefas = TarefaSerializer(many=True, read_only=True)
