from datetime import date
from decimal import Decimal

from portfolios.models import AssetPrice, Portfolio, PortfolioAsset


def get_portfolio_evolution(
    portfolio,
    start_date,
    end_date
):
    """
    Return portfolio evolution between two dates.
    """
    
    portfolio_assets = list(
        PortfolioAsset.objects.select_related("asset")
        .filter(portfolio=portfolio)
        .order_by("asset__name")
    )

    asset_ids = [portfolio_asset.asset_id for portfolio_asset in portfolio_assets]

    # Load prices for those assets in the requested period.
    prices = (
        AssetPrice.objects.select_related("asset")
        .filter(
            asset_id__in=asset_ids,
            date__gte=start_date,
            date__lte=end_date,
        )
        .order_by("date", "asset__name")
    )
    
    # Group prices by date and asset id.
    prices_by_date = {}

    for price in prices:        
        prices_by_date.setdefault(price.date, {})
        prices_by_date[price.date][price.asset_id] = price
        
    result = []

    # Build one response row per date
    for current_date, prices_for_date in prices_by_date.items():
        
        asset_entries = []
        portfolio_value = Decimal("0")

        for portfolio_asset in portfolio_assets:
            
            if portfolio_asset.initial_quantity is None:
                raise ValueError(
                    f"Falta la cantidad inicial para {portfolio_asset}"
                )

            price = prices_for_date.get(portfolio_asset.asset_id)

            if price is None:
                raise ValueError(
                    f"Falta el precio del activo {portfolio_asset.asset} en la fecha {current_date}"
                )

            
            asset_value = price.price * portfolio_asset.initial_quantity

            
            portfolio_value += asset_value

            
            asset_entries.append(
                {
                    "asset": portfolio_asset.asset.name,
                    "quantity": portfolio_asset.initial_quantity,
                    "price": price.price,
                    "asset_value": asset_value,
                }
            )

        if portfolio_value == 0:
            raise ValueError(
                f"El valor del portafolio es cero en la fecha {current_date}; no se pueden calcular los weights"
            )

        for asset_entry in asset_entries:
            asset_entry["weight"] = asset_entry["asset_value"] / portfolio_value

        result.append(
            {
                "date": current_date,
                "portfolio": portfolio.name,
                "portfolio_value": portfolio_value,
                "assets": asset_entries,
            }
        )

    return result
