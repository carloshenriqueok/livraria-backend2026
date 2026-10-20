from django.test import SimpleTestCase
from django.urls import reverse


class DocumentacaoTests(SimpleTestCase):
    def test_schema_disponivel_com_filtros_de_livros(self):
        response = self.client.get(reverse('schema'), HTTP_ACCEPT='application/vnd.oai.openapi+json')

        self.assertEqual(response.status_code, 200)
        schema = response.json()
        parametros = schema['paths']['/api/livros/']['get']['parameters']
        nomes = {parametro['name'] for parametro in parametros}
        self.assertIn('categoria__descricao', nomes)
        self.assertIn('editora__nome', nomes)

    def test_documentacao_disponivel(self):
        response = self.client.get(reverse('swagger-ui'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('schema'))
