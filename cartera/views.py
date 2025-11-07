from django.shortcuts import render
from django.core.paginator import Paginator
from datetime import datetime
from .utils.mssql_connector import obtener_cartera_vencida

def dashboard_cartera(request):
    fecha_corte_str = request.GET.get('fecha_corte')
    compania = request.GET.get('compania')
    filtro = request.GET.get('filtro', '').strip()
    ordenar = request.GET.get('ordenar', 'ValorTotal')
    resumen = []
    error = None

    if fecha_corte_str and compania:
        try:
            fecha_corte = datetime.strptime(fecha_corte_str, "%Y-%m-%d")
            df = obtener_cartera_vencida(fecha_corte_str, compania)  # Recibe DataFrame
            df['VENCFAC'] = pd.to_datetime(df['VENCFAC'], errors='coerce')

            # Agrupar por cliente y sumar valores
            agrupado = df.groupby(['IDCLIPRV', 'RAZONCIAL']).agg(
                PorVencer=('PorVencer', 'sum'),
                Treinta=('Treinta', 'sum'),
                Sesenta=('Sesenta', 'sum'),
                Noventa=('Noventa', 'sum'),
                CientoOchenta=('CientoOchenta', 'sum'),
                TresSesenta=('TresSesenta', 'sum'),
                MasNoventa=('MasNoventa', 'sum'),
                FechaMasAntigua=('VENCFAC', 'min')
            ).reset_index()

            # Total valor y días vencidos
            agrupado['ValorTotal'] = (
                agrupado['PorVencer'] + agrupado['Treinta'] + agrupado['Sesenta'] +
                agrupado['Noventa'] + agrupado['CientoOchenta'] +
                agrupado['TresSesenta'] + agrupado['MasNoventa']
            )
            agrupado['DiasVencidos'] = (fecha_corte - agrupado['FechaMasAntigua']).dt.days

            # Convierte a lista de dicts para el template
            resumen = agrupado[[
                'IDCLIPRV', 'RAZONCIAL', 'ValorTotal', 'DiasVencidos'
            ]].to_dict('records')

            # Filtro
            if filtro:
                filtro_lower = filtro.lower()
                resumen = [
                    r for r in resumen
                    if filtro_lower in str(r['IDCLIPRV']).lower()
                    or filtro_lower in str(r['RAZONCIAL']).lower()
                ]
            # Orden
            reverse = ordenar in ['ValorTotal', 'DiasVencidos']
            if ordenar in ['IDCLIPRV', 'RAZONCIAL']:
                resumen.sort(key=lambda x: str(x[ordenar]).lower())
            else:
                resumen.sort(key=lambda x: x[ordenar], reverse=reverse)
        except Exception as e:
            error = f"Error: {str(e)}"

    # Paginación
    paginator = Paginator(resumen, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "cartera/dashboard_cartera.html", {
        "page_obj": page_obj,
        "error": error,
        "fecha_corte": fecha_corte_str,
        "compania": compania,
        "filtro": filtro,
        "ordenar": ordenar,
    })