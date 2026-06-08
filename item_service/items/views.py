from django.http import JsonResponse
from items.services.item_service import ItemService
from items.gateways.divine_pride import DivinePrideGateway

item_service = ItemService(gateway=DivinePrideGateway())

def search_item(request):
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse({'status': 'error', 'message': 'Missing query parameter q'}, status=400)

    item, error_message = item_service.get_item(query)
                
    if error_message:
        status_code = 404 if "Nenhum" in error_message else 400
        return JsonResponse({'status': 'error', 'message': error_message}, status=status_code)
    
    if item:
        return JsonResponse({
            'status': 'success',
            'item': {
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
            }
        })
            
    return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
