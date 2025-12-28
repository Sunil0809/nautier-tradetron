"""FYERS broker adapter"""
import logging
from typing import Optional, Dict, Any
import requests
from urllib.parse import urlencode

logger = logging.getLogger(__name__)


class FyersClient:
    """FYERS API client wrapper"""
    
    BASE_URL = "https://api.fyers.in"
    AUTH_URL = "https://api-t1.fyers.in"
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None
        self.session = requests.Session()
    
    def get_auth_url(self, redirect_url: str) -> str:
        """Get OAuth login URL"""
        params = {
            "client_id": self.app_id,
            "redirect_uri": redirect_url,
            "response_type": "code",
            "scope": "full_access",
        }
        return f"{self.AUTH_URL}/api/v3/login?{urlencode(params)}"
    
    def get_access_token(self, code: str) -> Optional[str]:
        """Exchange auth code for access token"""
        try:
            response = requests.post(
                f"{self.AUTH_URL}/api/v3/token",
                json={
                    "code": code,
                    "client_id": self.app_id,
                    "client_secret": self.app_secret,
                    "grant_type": "authorization_code",
                },
            )
            response.raise_for_status()
            data = response.json()
            self.access_token = data.get("access_token")
            logger.info("Access token obtained")
            return self.access_token
        except Exception as e:
            logger.error(f"Failed to get access token: {e}")
            return None
    
    def place_order(
        self,
        symbol: str,
        order_type: str,
        side: str,
        quantity: int,
        price: float = 0,
        client_order_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Place market or limit order
        
        Args:
            symbol: e.g., "NSE:SBIN-EQ"
            order_type: "MARKET" or "LIMIT"
            side: "BUY" or "SELL"
            quantity: Order quantity
            price: Price (for LIMIT orders)
            client_order_id: Idempotent ID (crucial!)
        """
        if not self.access_token:
            logger.error("No access token")
            return {"status": "error", "message": "Not authenticated"}
        
        try:
            payload = {
                "symbol": symbol,
                "qty": quantity,
                "type": 1 if order_type == "MARKET" else 2,
                "side": 1 if side == "BUY" else -1,
                "productType": "MIS",  # Intraday
                "priceType": "0" if order_type == "MARKET" else "1",
                "price": price,
            }
            
            if client_order_id:
                payload["clientId"] = client_order_id
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            
            response = self.session.post(
                f"{self.BASE_URL}/api/v3/orders/place",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            
            order_data = response.json()
            logger.info(f"Order placed: {order_data}")
            return order_data
            
        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """Get order status"""
        if not self.access_token:
            return {"status": "error", "message": "Not authenticated"}
        
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
            }
            response = self.session.get(
                f"{self.BASE_URL}/api/v3/orders/{order_id}",
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get order status: {e}")
            return {"status": "error", "message": str(e)}
    
    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel order"""
        if not self.access_token:
            return {"status": "error", "message": "Not authenticated"}
        
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
            }
            response = self.session.delete(
                f"{self.BASE_URL}/api/v3/orders/{order_id}",
                headers=headers,
            )
            response.raise_for_status()
            logger.info(f"Order cancelled: {order_id}")
            return response.json()
        except Exception as e:
            logger.error(f"Failed to cancel order: {e}")
            return {"status": "error", "message": str(e)}
