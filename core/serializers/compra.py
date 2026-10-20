from django.db import transaction
from rest_framework.serializers import (
    CharField,
    CurrentUserDefault,
    DateTimeField,
    HiddenField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)

from core.models import Compra, ItensCompra


class ItensCompraCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade', 'preco')
        read_only_fields = ('preco',)

    def validate_quantidade(self, quantidade):
        if quantidade <= 0:
            raise ValidationError('A quantidade deve ser maior do que zero.')
        return quantidade

    def validate(self, item):
        if item.get('quantidade', 1) > item['livro'].quantidade:
            raise ValidationError('Quantidade de itens maior do que a quantidade em estoque.')
        return item


class ItensCompraSerializer(ModelSerializer):
    titulo = CharField(source='livro.titulo', read_only=True)
    editora = CharField(source='livro.editora', read_only=True)
    capa = CharField(source='livro.capa.url', read_only=True)
    total = SerializerMethodField()

    def get_total(self, item):
        return item.preco * item.quantidade

    class Meta:
        model = ItensCompra
        fields = ('titulo', 'editora', 'preco', 'quantidade', 'total', 'capa')


class ItensComprasSerializer(ItensCompraSerializer):
    pass


class ItensCompraListSerializer(ModelSerializer):
    livro = CharField(source='livro.titulo', read_only=True)

    class Meta:
        model = ItensCompra
        fields = ('quantidade', 'livro', 'preco')


class CompraCreateUpdateSerializer(ModelSerializer):
    usuario = HiddenField(default=CurrentUserDefault())
    itens = ItensCompraCreateUpdateSerializer(many=True)

    class Meta:
        model = Compra
        fields = ('usuario', 'itens')

    @transaction.atomic
    def create(self, validated_data):
        itens = validated_data.pop('itens')
        usuario = validated_data['usuario']

        compra, criada = Compra.objects.get_or_create(
            usuario=usuario, status=Compra.StatusCompra.CARRINHO, defaults=validated_data
        )

        for item in itens:
            item_existente = compra.itens.filter(livro=item['livro']).first()

            if item_existente:
                item_existente.quantidade += item['quantidade']
                item_existente.preco = item['livro'].preco
                item_existente.save()
            else:
                item['preco'] = item['livro'].preco
                ItensCompra.objects.create(compra=compra, **item)

        return compra

    @transaction.atomic
    def update(self, compra, validated_data):
        itens = validated_data.pop('itens', [])
        if itens:
            compra.itens.all().delete()
            for item in itens:
                item['preco'] = item['livro'].preco
                ItensCompra.objects.create(compra=compra, **item)

        return super().update(compra, validated_data)


class CompraListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItensCompraListSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'itens')


class CompraSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    status = CharField(source='get_status_display', read_only=True)
    data = DateTimeField(read_only=True)
    tipo_pagamento = CharField(source='get_tipo_pagamento_display', read_only=True)
    itens = ItensCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'status', 'itens', 'data', 'total', 'tipo_pagamento')
