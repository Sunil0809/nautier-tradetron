from .models import RiskProfile


def validate_order_risk(user_id: int, symbol: str, quantity: float) -> dict:
    profile, _ = RiskProfile.objects.get_or_create(user_id=user_id)
    if quantity > profile.max_position_size:
        return {'allowed': False, 'reason': 'max position exceeded'}
    return {'allowed': True, 'reason': ''}
