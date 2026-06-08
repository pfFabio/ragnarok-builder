from typing import List, Dict, Optional, Any
from builds.models import Build

class BuildService:
    @staticmethod
    def save_build(data: Dict[str, Any]) -> int:
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
        return build.id

    @staticmethod
    def get_all_builds() -> List[Dict[str, Any]]:
        return list(Build.objects.all().values('id', 'nome', 'classe', 'nivel'))

    @staticmethod
    def get_build_by_id(build_id: int) -> Optional[Dict[str, Any]]:
        try:
            build = Build.objects.get(id=build_id)
            return {
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
        except Build.DoesNotExist:
            return None
