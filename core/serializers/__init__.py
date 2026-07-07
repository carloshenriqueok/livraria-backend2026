from .autor import AutorSerializer
from .categoria import CategoriaSerializer
from .compra import (
    CompraSerializer,
    CompraCreateUpdateSerializer,
    ItensComprasSerializer,
    ItensCompraCreateUpdateSerializer,
    )
from .editora import EditoraSerializer
from .livro import LivroListSerializer, LivroRetrieveSerializer, LivroSerializer
from .user import UserRegistrationSerializer, UserSerializer
