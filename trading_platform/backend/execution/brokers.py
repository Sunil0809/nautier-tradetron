from dataclasses import dataclass


@dataclass
class BrokerOrder:
    symbol: str
    side: str
    quantity: float


class BaseBrokerAdapter:
    name = 'base'

    def place_order(self, order: BrokerOrder) -> dict:
        return {'status': 'accepted', 'broker': self.name, 'order': order.__dict__}


class UpstoxAdapter(BaseBrokerAdapter):
    name = 'upstox'


class FyersAdapter(BaseBrokerAdapter):
    name = 'fyers'


class ZerodhaAdapter(BaseBrokerAdapter):
    name = 'zerodha'


def get_adapter(broker: str) -> BaseBrokerAdapter:
    mapping = {'upstox': UpstoxAdapter(), 'fyers': FyersAdapter(), 'zerodha': ZerodhaAdapter()}
    return mapping[broker.lower()]
