from app.db.models import Package


def compute_delivery_status(pkg: Package) -> str:
    if pkg.delivery_calculated and pkg.delivery_price_rub is not None:
        return f"{pkg.delivery_price_rub:.2f}"
    return "Не рассчитано"
