import json

from rest_framework.test import APITestCase


class TestListUsuarios(APITestCase):
    def test_listagem_vazia(self):
        response = self.client.get('/api/usuarios/')
        self.assertEqual(json.loads(response.content), [])
