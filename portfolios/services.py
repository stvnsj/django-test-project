from datetime import date
from decimal import Decimal

from portfolios.models import AssetPrice, Portfolio, PortfolioAsset


def get_portfolio_evolution(
    portfolio: Portfolio,
    start_date: date,
    end_date: date,
) :
    """
    Portfolio data between start_date and end_date.
    """

    # Get all portfolio_asset, with associated asset, matching the portfolio.
    portfolio_assets = list(
        PortfolioAsset.objects.select_related("asset")
        .filter(portfolio=portfolio)
        .order_by("asset__name")
    )

    # get all asset id's belonging to the portfolio.
    asset_ids = [portfolio_asset.asset_id for portfolio_asset in portfolio_assets]


    # Get all asset_price's with the associated assets.
    # between start_date and end_date, and mathching
    # one of asset_ids
    prices = (
        AssetPrice.objects.select_related("asset")
        .filter(
            asset_id__in=asset_ids,
            date__gte=start_date,
            date__lte=end_date,
        )
        .order_by("date", "asset__name")
    )
    
    # e.g. prices_by_date["2022-09-02"][12] -> price
    prices_by_date: dict[date, dict[int, AssetPrice]] = {}

    
    for price in prices:
        # set empty dictionary for each date
        prices_by_date.setdefault(price.date, {})
        # for each date and asset_id, set price
        prices_by_date[price.date][price.asset_id] = price
        

    result = []

    # Destructure date and prices_for_date.
    # prices_for_date is the dictionary of all asset prices for
    # the given date.
    for current_date, prices_for_date in prices_by_date.items():
        
        asset_entries = []
        portfolio_value = Decimal("0") # Initial porfolio value on current date

        for portfolio_asset in portfolio_assets:
            if portfolio_asset.initial_quantity is None:
                raise ValueError(
                    f"Missing initial quantity for {portfolio_asset}"
                )

            # for the asset in the portfolio, retrieve AssetPrice
            price = prices_for_date.get(portfolio_asset.asset_id)

            if price is None:
                continue

            # Asset Value 
            asset_value = price.price * portfolio_asset.initial_quantity

            # Portfolio value
            portfolio_value += asset_value

            # Quantity, price and asset value
            asset_entries.append(
                {
                    "asset": portfolio_asset.asset.name,
                    "quantity": portfolio_asset.initial_quantity,
                    "price": price.price,
                    "asset_value": asset_value,
                }
            )

        if portfolio_value == 0:
            continue

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
