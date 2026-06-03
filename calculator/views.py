import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from calculator.services.item_service import ItemService, ItemCache
from calculator.gateways.divine_pride import DivinePrideGateway
from calculator.services.build_service import BuildService

# Injeção de dependência manual (Poderia ser via um container de DI)
item_service = ItemService(gateway=DivinePrideGateway(), cache=ItemCache())

def index(request):
    return render(request, 'index.html')

def search_item(request):
    query = request.GET.get('q', '').strip()
    items = []
    error_message = None
    
    if not query:
        return render(request, 'item_results.html', {'items': items, 'query': query})

    item, error_message = item_service.get_item(query)
                
    if item:
        items.append({
            'id': item.id,
            'name': item.name,
            'icon': item.icon_url,
            'attack': item.attack,
            'defense': item.defense,
            'str': item.str_bonus,
            'agi': item.agi_bonus,
            'vit': item.vit_bonus,
            'int': item.int_bonus,
            'dex': item.dex_bonus,
            'luk': item.luk_bonus,
        })
            
    return render(request, 'item_results.html', {'items': items, 'query': query, 'error_message': error_message})

@csrf_exempt
def save_build(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'invalid method'}, status=405)
        
    try:
        data = json.loads(request.body)
        build_id = BuildService.save_build(data)
        return JsonResponse({'status': 'success', 'build_id': build_id})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def list_builds(request):
    builds = BuildService.get_all_builds()
    return JsonResponse({'builds': builds})

def load_build(request, build_id):
    build_data = BuildService.get_build_by_id(build_id)
    if build_data:
        return JsonResponse({'status': 'success', 'build': build_data})
    return JsonResponse({'status': 'error', 'message': 'Build não encontrada'}, status=404)
