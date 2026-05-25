#!/usr/bin/env python3
"""
MCP Tool Template

This module provides a template for creating individual MCP tools.
Each tool represents a single capability that can be exposed to AI models.

Tool Structure:
1. Tool Definition (Schema)
2. Input Validation
3. Business Logic
4. Error Handling
5. Result Formatting
"""

import json
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod


class MCPTool(ABC):
    """
    Abstract base class for MCP tools.
    
    All MCP tools should inherit from this class and implement
    the required methods.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name (unique identifier)"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable tool description"""
        pass
    
    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        """JSON Schema for input parameters"""
        pass
    
    @abstractmethod
    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the tool.
        
        Args:
            arguments: Input arguments matching the schema
            
        Returns:
            Result dictionary
        """
        pass
    
    def get_definition(self) -> Dict[str, Any]:
        """
        Get complete tool definition.
        
        Returns:
            Tool definition for registration
        """
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema
        }
    
    def validate_arguments(self, arguments: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate arguments against schema.
        
        Args:
            arguments: Arguments to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        schema = self.input_schema
        required = schema.get("required", [])
        properties = schema.get("properties", {})
        
        # Check required fields
        for field in required:
            if field not in arguments:
                return False, f"Missing required field: {field}"
        
        # Check field types (basic validation)
        for field, value in arguments.items():
            if field not in properties:
                return False, f"Unknown field: {field}"
            
            expected_type = properties[field].get("type")
            # Simple type checking
            if expected_type == "string" and not isinstance(value, str):
                return False, f"Field {field} must be string"
            elif expected_type == "number" and not isinstance(value, (int, float)):
                return False, f"Field {field} must be number"
            elif expected_type == "boolean" and not isinstance(value, bool):
                return False, f"Field {field} must be boolean"
        
        return True, ""


class SimpleExampleTool(MCPTool):
    """
    Example: A simple tool that adds two numbers.
    
    Demonstrates:
    - Tool definition
    - Schema validation
    - Result formatting
    """
    
    @property
    def name(self) -> str:
        return "add_numbers"
    
    @property
    def description(self) -> str:
        return "Adds two numbers together"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "number1": {
                    "type": "number",
                    "description": "First number"
                },
                "number2": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["number1", "number2"]
        }
    
    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the add_numbers tool.
        """
        # Validate arguments
        is_valid, error = self.validate_arguments(arguments)
        if not is_valid:
            return {
                "status": "error",
                "message": error
            }
        
        try:
            num1 = float(arguments["number1"])
            num2 = float(arguments["number2"])
            result = num1 + num2
            
            return {
                "status": "success",
                "number1": num1,
                "number2": num2,
                "result": result
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Execution failed: {str(e)}"
            }


class AdvancedExampleTool(MCPTool):
    """
    Example: A more complex tool with multiple parameters.
    
    Demonstrates:
    - Complex schema with enums
    - Optional parameters
    - Advanced logic
    """
    
    @property
    def name(self) -> str:
        return "calculate"
    
    @property
    def description(self) -> str:
        return "Performs mathematical calculations (add, subtract, multiply, divide)"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "operand1": {
                    "type": "number",
                    "description": "First operand"
                },
                "operand2": {
                    "type": "number",
                    "description": "Second operand"
                },
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "Operation to perform"
                },
                "round_result": {
                    "type": "boolean",
                    "description": "Whether to round the result (optional)"
                }
            },
            "required": ["operand1", "operand2", "operation"]
        }
    
    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the calculate tool.
        """
        is_valid, error = self.validate_arguments(arguments)
        if not is_valid:
            return {"status": "error", "message": error}
        
        try:
            op1 = float(arguments["operand1"])
            op2 = float(arguments["operand2"])
            operation = arguments["operation"]
            should_round = arguments.get("round_result", False)
            
            # Perform calculation
            if operation == "add":
                result = op1 + op2
            elif operation == "subtract":
                result = op1 - op2
            elif operation == "multiply":
                result = op1 * op2
            elif operation == "divide":
                if op2 == 0:
                    return {
                        "status": "error",
                        "message": "Division by zero not allowed"
                    }
                result = op1 / op2
            else:
                return {
                    "status": "error",
                    "message": f"Unknown operation: {operation}"
                }
            
            # Round if requested
            if should_round:
                result = round(result, 2)
            
            return {
                "status": "success",
                "operand1": op1,
                "operand2": op2,
                "operation": operation,
                "result": result
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Execution failed: {str(e)}"
            }


# Example usage and testing
if __name__ == "__main__":
    print("\n" + "="*60)
    print("MCP TOOL TEMPLATE - DEMONSTRATION")
    print("="*60)
    
    # Test Simple Tool
    print("\n📦 Simple Tool: Add Numbers")
    print("-" * 60)
    simple_tool = SimpleExampleTool()
    print(f"Name: {simple_tool.name}")
    print(f"Description: {simple_tool.description}")
    print(f"Schema: {json.dumps(simple_tool.input_schema, indent=2)}")
    
    print("\nExecuting: add_numbers(5, 3)")
    result = simple_tool.execute({"number1": 5, "number2": 3})
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Test Advanced Tool
    print("\n📦 Advanced Tool: Calculate")
    print("-" * 60)
    advanced_tool = AdvancedExampleTool()
    print(f"Name: {advanced_tool.name}")
    print(f"Description: {advanced_tool.description}")
    
    print("\nExecuting: calculate(10, 3, 'divide', round_result=True)")
    result = advanced_tool.execute({
        "operand1": 10,
        "operand2": 3,
        "operation": "divide",
        "round_result": True
    })
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Show error handling
    print("\nExecuting: calculate(10, 0, 'divide') - Division by zero")
    result = advanced_tool.execute({
        "operand1": 10,
        "operand2": 0,
        "operation": "divide"
    })
    print(f"Result: {json.dumps(result, indent=2)}")
    
    print("\n✅ Tool demonstrations completed!\n")
