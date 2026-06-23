from rest_framework.serializers import CharField, ModelSerializer

from core.models import Compra, ItensCompra

class ItensComprasSerializer(ModelSerializer):
    titulo = CharField(source='livro.titulo', read_only=True)
    preco = CharField(source='livro.preco', read_only=True)
    editora = CharField(source='livro.editora', read_only=True)
    
    class Meta:
        model = ItensCompra
        fields = ('quantidade', 'titulo', 'preco', 'editora')

class CompraSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    status = CharField(source='get_status_display', read_only=True)
    itens = ItensComprasSerializer(many=True, read_only=True)
    
    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'status', 'itens')