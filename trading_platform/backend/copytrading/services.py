def scaled_quantity(master_qty: float, allocation_pct: float, risk_scale: float) -> float:
    return max(master_qty * allocation_pct * risk_scale, 0)
