from .autor import AutorSerializer
from .categoria import CategoriaSerializer
from .compra import (
    CompraCreateUpdateSerializer,
    CompraListSerializer, # novo
    CompraSerializer,
    ItensCompraCreateUpdateSerializer,
    ItensCompraListSerializer, # novo
    ItensComprasSerializer,
)
from .editora import EditoraSerializer
from .livro import LivroListSerializer, LivroRetrieveSerializer, LivroSerializer
from .user import UserRegistrationSerializer, UserSerializer
