from datetime import date
from decimal import Decimal

from portfolios.models import AssetPrice, Portfolio, PortfolioAsset


def get_portfolio_evolution(
    portfolio: Portfolio,
    start_date: date,
    end_date: date,
) :

    # get all assets 
    portfolio_assets = list(
        PortfolioAsset.objects.select_related("asset")
        .filter(portfolio=portfolio)
        .order_by("asset__name")
    )
    
    asset_ids = [portfolio_asset.asset_id for portfolio_asset in portfolio_assets]

    prices = (
        AssetPrice.objects.select_related("asset")
        .filter(
            asset_id__in=asset_ids,
            date__gte=start_date,
            date__lte=end_date,
        )
        .order_by("date", "asset__name")
    )

    prices_by_date: dict[date, dict[int, AssetPrice]] = {}

    for price in prices:
        prices_by_date.setdefault(price.date, {})
        prices_by_date[price.date][price.asset_id] = price

    result = []

    for current_date, prices_for_date in prices_by_date.items():
        holdings = []
        portfolio_value = Decimal("0")

        for portfolio_asset in portfolio_assets:
            if portfolio_asset.initial_quantity is None:
                raise ValueError(
                    f"Missing initial quantity for {portfolio_asset}"
                )

            price = prices_for_date.get(portfolio_asset.asset_id)

            if price is None:
                continue

            holding_value = price.price * portfolio_asset.initial_quantity
            portfolio_value += holding_value

            holdings.append(
                {
                    "asset": portfolio_asset.asset.name,
                    "quantity": portfolio_asset.initial_quantity,
                    "price": price.price,
                    "holding_value": holding_value,
                }
            )

        if portfolio_value == 0:
            continue

        for holding in holdings:
            holding["weight"] = holding["holding_value"] / portfolio_value

        result.append(
            {
                "date": current_date,
                "portfolio": portfolio.name,
                "portfolio_value": portfolio_value,
                "holdings": holdings,
            }
        )

    return result
