import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from builds.services.build_service import BuildService

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

@csrf_exempt
def delete_build(request, build_id):
    if request.method != 'DELETE':
        return JsonResponse({'status': 'invalid method'}, status=405)
        
    success = BuildService.delete_build(build_id)
    if success:
        return JsonResponse({'status': 'success', 'message': 'Build deletada com sucesso'})
    return JsonResponse({'status': 'error', 'message': 'Build não encontrada'}, status=404)
