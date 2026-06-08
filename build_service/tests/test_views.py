import pytest
from django.urls import reverse
from builds.models import Build
import json

@pytest.fixture
def api_client():
    from django.test import Client
    return Client()

@pytest.mark.django_db
def test_save_build_success(api_client):
    url = reverse('save_build')
    payload = {
        'nome': 'Build Matadora',
        'classe': 'cavaleiro',
        'nivel': '99',
        'transclasse': False,
        'str': '90',
        'agi': '90',
        'vit': '1',
        'int': '1',
        'dex': '40',
        'luk': '1',
        'equipamentos': {'mao_direita': '1201'}
    }
    
    response = api_client.post(url, data=json.dumps(payload), content_type='application/json')
    
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    
    # Verify in DB
    build = Build.objects.get(id=data['build_id'])
    assert build.nome == 'Build Matadora'
    assert build.classe == 'cavaleiro'
    assert build.equipamentos['mao_direita'] == '1201'

@pytest.mark.django_db
def test_list_builds(api_client):
    Build.objects.create(nome='Build 1', classe='bruxo', equipamentos={})
    Build.objects.create(nome='Build 2', classe='cavaleiro', equipamentos={})

    url = reverse('list_builds')
    response = api_client.get(url)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data['builds']) == 2
    assert data['builds'][0]['nome'] == 'Build 1'

@pytest.mark.django_db
def test_load_build(api_client):
    b = Build.objects.create(
        nome='Test Load',
        classe='sacerdote',
        inteligencia=99,
        forca=1,
        equipamentos={'topo': '100'}
    )

    url = reverse('load_build', args=[b.id])
    response = api_client.get(url)
    
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert data['build']['nome'] == 'Test Load'
    assert data['build']['classe'] == 'sacerdote'
    assert data['build']['atributos']['int'] == 99
