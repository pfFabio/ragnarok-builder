import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from django.urls import reverse
from builds.models import Build
import json

pytestmark = pytest.mark.django_db

scenarios('../features/save_build.feature')

@pytest.fixture
def api_client():
    from django.test import Client
    return Client()

@pytest.fixture
def payload():
    return {}

@given(parsers.parse('que eu preenchi os dados do meu "{classe}" nivel {nivel:d} chamado "{nome}"'))
def setup_payload(payload, classe, nivel, nome):
    payload.update({
        'nome': nome,
        'classe': classe,
        'nivel': str(nivel),
        'transclasse': False,
        'str': '1', 'agi': '1', 'vit': '1', 'int': '1', 'dex': '1', 'luk': '1',
        'equipamentos': {}
    })

@when('eu envio a requisicao para salvar a build', target_fixture="response")
def enviar_requisicao(api_client, payload):
    url = reverse('save_build')
    return api_client.post(url, data=json.dumps(payload), content_type='application/json')

@then('a build deve ser salva no banco de dados e retornar sucesso')
def verificar_salvamento(response):
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    build = Build.objects.get(id=data['build_id'])
    assert build is not None
    assert build.nome == "Build Teste"
