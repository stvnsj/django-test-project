from datetime import date

from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render

from portfolios.models import Portfolio
from portfolios.services import get_portfolio_evolution




def parse_date(value):
    return date.fromisoformat(value)


def portfolio_evolution_api(request: HttpRequest, portfolio_id: int) -> JsonResponse:
    raw_start_date = request.GET.get("fecha_inicio")
    raw_end_date = request.GET.get("fecha_fin")

    if raw_start_date is None or raw_end_date is None:
        return JsonResponse(
            {
                "error": "fecha_inicio and fecha_fin are required. Use YYYY-MM-DD format."
            },
            status=400,
        )

    try:
        start_date = parse_date(raw_start_date)
        end_date = parse_date(raw_end_date)
    except ValueError:
        return JsonResponse(
            {
                "error": "Invalid date format. Use YYYY-MM-DD."
            },
            status=400,
        )

    if start_date > end_date:
        return JsonResponse(
            {
                "error": "fecha_inicio must be before or equal to fecha_fin."
            },
            status=400,
        )

    portfolio = get_object_or_404(Portfolio, id=portfolio_id)

    data = get_portfolio_evolution(
        portfolio=portfolio,
        start_date=start_date,
        end_date=end_date,
    )

    return JsonResponse(
        {
            "portfolio": portfolio.name,
            "fecha_inicio": start_date,
            "fecha_fin": end_date,
            "data": data,
        }
    )



def comparison_view(request):
    portfolio_1 = get_object_or_404(Portfolio, name="Portfolio 1")
    portfolio_2 = get_object_or_404(Portfolio, name="Portfolio 2")

    return render(
        request,
        "portfolios/comparison.html",
        {
            "portfolio_1_id": portfolio_1.id,
            "portfolio_2_id": portfolio_2.id,
            "start_date": "2022-02-15",
            "end_date": "2023-02-16",
        },
    )
