
from django.urls import path

from portfolios import views

app_name = "portfolios"

urlpatterns = [
    
    path(
        "api/portfolios/<int:portfolio_id>/evolution/",
        views.portfolio_evolution_api,
        name="portfolio_evolution_api",
    ),
    
    path(
        "comparison/",
        views.comparison_view,
        name="comparison",
    )
]
