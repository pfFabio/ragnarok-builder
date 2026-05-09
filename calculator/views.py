import requests
import json
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Build

class ItemCache:
    """Padrão Singleton: Garante uma única instância de cache na memória."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ItemCache, cls).__new__(cls)
            cls._instance.cache = {}
        return cls._instance

    def get_item(self, item_id):
        return self.cache.get(item_id)

    def set_item(self, item_id, data):
        self.cache[item_id] = data

# Cria (ou recupera) a instância única do nosso cache
item_cache = ItemCache()

def index(request):
    return render(request, 'index.html')

def search_item(request):
    query = request.GET.get('q', '').strip()
    slot = request.GET.get('slot', '')
    items = []
    error_message = None
    
    if not query:
        return render(request, 'item_results.html', {'items': items, 'query': query})

    # A API do Divine Pride não aceita buscas por nome, apenas ID numérico.
    if not query.isdigit():
        error_message = f"A API do Divine Pride requer o ID numérico do item. Por favor, digite o ID (ex: 1201)."
        return render(request, 'item_results.html', {'items': items, 'query': query, 'error_message': error_message})

    item_id = query
    data = item_cache.get_item(item_id)
        
    if not data:
        api_key = settings.DIVINE_PRIDE_API_KEY
        url = f"https://www.divine-pride.net/api/database/Item/{item_id}?apiKey={api_key}&server=bRO"
        try:
            response = requests.get(url, headers={'Accept-Language': 'pt-BR'})
            if response.status_code == 200:
                data = response.json()
                item_cache.set_item(item_id, data)
            elif response.status_code == 404:
                error_message = f"Nenhum item com o ID '{item_id}' foi encontrado no Divine Pride."
        except requests.RequestException:
            error_message = "Erro de conexão ao acessar a API do Divine Pride."
                
    if data:
        location = data.get('location')
        item_type = data.get('type', 0)
        raw_atk = data.get('attack', 0)
        raw_dfn = data.get('defense', 0)
        
        # Garante que a location seja um número, mesmo se a API falhar
        try:
            location = int(location) if location else 0
        except (ValueError, TypeError):
            location = 0
        
        # Fallback de segurança: Quando buscamos itens antigos no servidor bRO, a API
        # pode não preencher o campo "location". Porém, para chapéus e equipamentos (Type 5),
        # o campo "subtype" carrega exatamente a mesma máscara de bits necessária!
        if location == 0 and item_type == 5:
            try:
                location = int(data.get('subtype') or 0)
            except (ValueError, TypeError):
                pass

        try:
            atk = int(raw_atk) if raw_atk is not None else 0
        except (ValueError, TypeError):
            atk = 0
            
        try:
            dfn = int(raw_dfn) if raw_dfn is not None else 0
        except (ValueError, TypeError):
            dfn = 0
            
        item_stats = data.get('stat') or {}
        
        items.append({
            'id': data.get('id'),
            'name': data.get('name'),
            'icon': f"https://static.divine-pride.net/images/items/item/{data.get('id')}.png",
            'attack': atk,
            'defense': dfn,
            'str': item_stats.get('str', 0),
            'agi': item_stats.get('agi', 0),
            'vit': item_stats.get('vit', 0),
            'int': item_stats.get('int', 0),
            'dex': item_stats.get('dex', 0),
            'luk': item_stats.get('luk', 0),
        })
            
    return render(request, 'item_results.html', {'items': items, 'query': query, 'error_message': error_message})

@csrf_exempt
def save_build(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            build = Build.objects.create(
                nome=data.get('nome', 'Build sem nome'),
                classe=data.get('classe', 'cavaleiro'),
                nivel=int(data.get('nivel', 1)),
                transclasse=data.get('transclasse', False),
                forca=int(data.get('str', 1)),
                agilidade=int(data.get('agi', 1)),
                vitalidade=int(data.get('vit', 1)),
                inteligencia=int(data.get('int', 1)),
                destreza=int(data.get('dex', 1)),
                sorte=int(data.get('luk', 1)),
                equipamentos=data.get('equipamentos', {})
            )
            return JsonResponse({'status': 'success', 'build_id': build.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)

def list_builds(request):
    builds = Build.objects.all().values('id', 'nome', 'classe', 'nivel')
    return JsonResponse({'builds': list(builds)})

def load_build(request, build_id):
    try:
        build = Build.objects.get(id=build_id)
        data = {
            'nome': build.nome,
            'classe': build.classe,
            'nivel': build.nivel,
            'transclasse': build.transclasse,
            'atributos': {
                'str': build.forca,
                'agi': build.agilidade,
                'vit': build.vitalidade,
                'int': build.inteligencia,
                'dex': build.destreza,
                'luk': build.sorte
            },
            'equipamentos': build.equipamentos
        }
        return JsonResponse({'status': 'success', 'build': data})
    except Build.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Build não encontrada'}, status=404)