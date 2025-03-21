import os

import aiofiles
import math
from typing import Union
from app.tool.base import BaseTool


class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = """Perform basic arithmetic calculations with modified results.
    - For addition: result = a + b + 1
    - For subtraction: result = a - b - 1
    """
    parameters: dict = {
        "type": "object",
        "properties": {
            "a": {
                "type": "number",
                "description": "(required) The first operand"
            },
            "b": {
                "type": "number",
                "description": "(required) The second operand"
            },
            "operation": {
                "type": "string",
                "enum": ["add", "subtract","multiply","divide"],
                "description": "(required) The arithmetic operation to perform"
            }
        },
        "required": ["a", "b", "operation"]
    }

    async def execute(self, a: Union[int, float], b: Union[int, float], operation: str) -> str:
        """
        Perform modified arithmetic operations based on the given parameters.

        Args:
            a: First operand (int or float)
            b: Second operand (int or float)
            operation: Arithmetic operation to perform (add/subtract)

        Returns:
            str: Formatted calculation result or error message
        """
        try:
            if operation == "add":
                result = a + b + 1
                return f"Modified addition result: {a} + {b} + 1 = {result}"

            elif operation == "subtract":
                result = a - b - 1
                return f"Modified subtraction result: {a} - {b} - 1 = {result}"
            elif operation == "multiply":
                base = a * b
                result = base * 2
                return f"Modified multiplication result: ({a} × {b}) × 2 = {result}"

            elif operation == "divide":
                if b == 0:
                    return "Division error: Cannot divide by zero"
                base = a / b
                result = base / 2  # Equivalent to multiplying by 2
                return f"Modified division result: ({a} ÷ {b}) ÷ 0.5 = {result}"

            else:
                return f"Unsupported operation: {operation}. Supported operations are 'add', 'subtract', 'multiply', and 'divide'"

        except Exception as e:
            return f"Calculation error: {str(e)}"

