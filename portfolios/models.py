from decimal import Decimal
from django.core import validators
from django.db import models


class Asset(models.Model):
    
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) :
        return self.name

class Portfolio(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    
    initial_value = models.DecimalField(max_digits=20, decimal_places=8)
    
    start_date = models.DateField()

    class Meta:
        ordering = ["name"]

    def __str__(self) :
        return self.name


class AssetPrice(models.Model):
    
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="prices",
    )
    
    date = models.DateField()
    
    price = models.DecimalField(max_digits=20, decimal_places=4)

    class Meta :
        ordering = ["date", "asset__name"]
        constraints=[
            models.UniqueConstraint(
                fields=["asset", "date"],
                name="unique_asset_price_per_date"
            )
        ]

    
    def __str__(self):
        return f"{self.asset} - {self.date}: {self.price}"

        

class PortfolioAsset(models.Model):
    
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="portfolio_assets"
    )
    
    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name="portfolio_assets"
    )

    initial_weight = models.DecimalField(
        max_digits=12,
        decimal_places=10,
        validators=[
            validators.MinValueValidator(Decimal("0")),
            validators.MaxValueValidator(Decimal("1"))
        ]
    )

    initial_quantity = models.DecimalField(
        max_digits=24,
        decimal_places=10,
        null=True, # database can store NULL
        blank=True
    )

    class Meta :
        ordering = ["portfolio__name", "asset__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["portfolio","asset"],
                name="unique_asset_per_portfolio"
            )
        ]

        
    def __str__(self):
        return f"{self.portfolio} - {self.asset}"
