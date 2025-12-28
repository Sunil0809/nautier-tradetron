"""Tradetron-style rule engine for no-code strategy building"""
import logging
from typing import Dict, Any, Optional, List
from enum import Enum
import json

logger = logging.getLogger(__name__)


class ComparisonOp(Enum):
    """Supported comparison operators"""
    EQ = "=="
    NE = "!="
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="
    CROSS_ABOVE = "CROSS_ABOVE"
    CROSS_BELOW = "CROSS_BELOW"


class RuleCondition:
    """Single rule condition
    
    Example:
    {
        "left": "EMA(9)",
        "op": "CROSS_ABOVE",
        "right": "EMA(21)"
    }
    """
    
    def __init__(self, left: str, op: str, right):
        self.left = left
        self.op = op
        self.right = right
    
    def evaluate(self, data: Dict[str, float]) -> bool:
        """Evaluate condition against data
        
        Args:
            data: Dict with indicator values, e.g., {"EMA_9": 100, "EMA_21": 99}
        
        Returns:
            True if condition is met
        """
        left_val = self._resolve_value(self.left, data)
        right_val = self._resolve_value(self.right, data)
        
        if left_val is None or right_val is None:
            logger.warning(f"Missing data for condition: {self.left} {self.op} {self.right}")
            return False
        
        op = self.op.upper()
        
        if op == "==":
            return left_val == right_val
        elif op == "!=":
            return left_val != right_val
        elif op == "<":
            return left_val < right_val
        elif op == "<=":
            return left_val <= right_val
        elif op == ">":
            return left_val > right_val
        elif op == ">=":
            return left_val >= right_val
        elif op == "CROSS_ABOVE":
            # Requires prev values: left was below right, now above
            return self._cross_above(left_val, right_val, data)
        elif op == "CROSS_BELOW":
            return self._cross_below(left_val, right_val, data)
        else:
            logger.error(f"Unknown operator: {op}")
            return False
    
    def _resolve_value(self, expr: str, data: Dict[str, float]) -> Optional[float]:
        """Resolve value from expression or data
        
        Examples:
        - "EMA(9)" → looks for EMA_9 in data
        - "70" → returns 70.0
        """
        
        # Try direct number
        try:
            return float(expr)
        except ValueError:
            pass
        
        # Try indicator format: "EMA(9)" → "EMA_9"
        if "(" in expr and ")" in expr:
            indicator = expr.replace("(", "_").replace(")", "")
            return data.get(indicator)
        
        # Try raw key
        return data.get(expr)
    
    def _cross_above(self, left: float, right: float, data: Dict) -> bool:
        """Check if left crossed above right"""
        # Simplified: just check if left > right
        # In production, maintain state of previous values
        return left > right
    
    def _cross_below(self, left: float, right: float, data: Dict) -> bool:
        """Check if left crossed below right"""
        return left < right


class Rule:
    """Complete rule with conditions and action
    
    Example:
    {
        "name": "EMA Crossover",
        "conditions": [
            {"left": "EMA(9)", "op": "CROSS_ABOVE", "right": "EMA(21)"},
            {"left": "RSI(14)", "op": "<", "right": 70}
        ],
        "operator": "AND",
        "action": "BUY"
    }
    """
    
    def __init__(self, name: str, conditions: List[Dict], action: str, operator: str = "AND"):
        self.name = name
        self.conditions = [
            RuleCondition(c["left"], c["op"], c["right"])
            for c in conditions
        ]
        self.action = action.upper()  # BUY, SELL, NONE
        self.operator = operator.upper()  # AND, OR
    
    def evaluate(self, data: Dict[str, float]) -> bool:
        """Evaluate rule against market data
        
        Returns:
            True if all conditions (AND) or any condition (OR) are met
        """
        if not self.conditions:
            return False
        
        results = [c.evaluate(data) for c in self.conditions]
        
        if self.operator == "AND":
            return all(results)
        elif self.operator == "OR":
            return any(results)
        else:
            logger.error(f"Unknown operator: {self.operator}")
            return False


class RuleEngine:
    """Rule engine for no-code strategy
    
    ❌ Never uses eval()
    ✅ Type-safe evaluation
    """
    
    def __init__(self):
        self.rules: Dict[int, Rule] = {}  # rule_id -> Rule
    
    def parse_rule_json(self, rule_json: str) -> Optional[Rule]:
        """Parse rule from JSON string
        
        ❌ NEVER use eval()
        ✅ Explicit parsing
        """
        try:
            data = json.loads(rule_json)
            rule = Rule(
                name=data.get("name", "Unnamed"),
                conditions=data.get("conditions", []),
                action=data.get("action", "NONE"),
                operator=data.get("operator", "AND"),
            )
            logger.info(f"Rule parsed: {rule.name}")
            return rule
        except Exception as e:
            logger.error(f"Failed to parse rule: {e}")
            return None
    
    def register_rule(self, rule_id: int, rule_json: str) -> bool:
        """Register rule by parsing JSON"""
        rule = self.parse_rule_json(rule_json)
        if rule:
            self.rules[rule_id] = rule
            return True
        return False
    
    def evaluate(self, rule_id: int, market_data: Dict[str, float]) -> Optional[str]:
        """Evaluate rule, return signal (BUY/SELL/NONE)
        
        Args:
            rule_id: Rule to evaluate
            market_data: Dict of indicators, e.g., {"EMA_9": 100, "EMA_21": 99, "RSI_14": 65}
        
        Returns:
            "BUY", "SELL", or "NONE"
        """
        rule = self.rules.get(rule_id)
        if not rule:
            logger.error(f"Rule {rule_id} not found")
            return "NONE"
        
        if rule.evaluate(market_data):
            logger.info(f"Rule {rule.name} triggered: {rule.action}")
            return rule.action
        
        return "NONE"
    
    def evaluate_all(self, market_data: Dict[str, float]) -> Dict[int, str]:
        """Evaluate all registered rules
        
        Returns:
            Dict of rule_id -> signal
        """
        results = {}
        for rule_id, rule in self.rules.items():
            results[rule_id] = "BUY" if rule.evaluate(market_data) else "NONE"
        return results
