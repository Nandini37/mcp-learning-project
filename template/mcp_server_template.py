#!/usr/bin/env python3
"""
MCP Server Template

This is a template for building an MCP (Model Context Protocol) server.
Use this as a starting point for your own MCP implementations.

Key Components:
1. Server initialization
2. Tool definitions with JSON schema
3. Tool execution handlers
4. Error handling and logging
"""

import json
import logging
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPServerTemplate:
    """
    Template for MCP Server implementation.
    
    This class demonstrates:
    - How to define tools
    - How to handle tool calls
    - How to manage resources
    """
    
    def __init__(self, server_name: str = "TemplateServer"):
        """
        Initialize the MCP server.
        
        Args:
            server_name: Name of the server for logging
        """
        self.server_name = server_name
        self.tools: List[Dict[str, Any]] = []
        self.initialized = False
        logger.info(f"Initializing {server_name}")
    
    def define_tools(self) -> None:
        """
        Define all available tools.
        
        This method should be overridden in child classes.
        Each tool needs:
        - name: Unique identifier
        - description: What it does (for AI models)
        - inputSchema: JSON Schema for parameters
        """
        
        # Example Tool 1: Simple Echo
        echo_tool = {
            "name": "echo",
            "description": "Echoes back the input message",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to echo"
                    }
                },
                "required": ["message"]
            }
        }
        self.tools.append(echo_tool)
        logger.info(f"Registered tool: {echo_tool['name']}")
        
        # Example Tool 2: Parameter Processor
        process_tool = {
            "name": "process_data",
            "description": "Processes data with optional transformation",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "Data to process"
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["uppercase", "lowercase", "reverse"],
                        "description": "Operation to perform on data"
                    }
                },
                "required": ["data", "operation"]
            }
        }
        self.tools.append(process_tool)
        logger.info(f"Registered tool: {process_tool['name']}")
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """
        Get list of available tools.
        
        Returns:
            List of tool definitions
        """
        if not self.tools:
            self.define_tools()
        return self.tools
    
    def execute_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a tool with given arguments.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments for the tool
            
        Returns:
            Result dictionary with status and data
        """
        try:
            logger.info(f"Executing tool: {tool_name} with args: {arguments}")
            
            if tool_name == "echo":
                return self._execute_echo(arguments)
            
            elif tool_name == "process_data":
                return self._execute_process_data(arguments)
            
            else:
                return {
                    "status": "error",
                    "message": f"Unknown tool: {tool_name}"
                }
        
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return {
                "status": "error",
                "message": f"Tool execution failed: {str(e)}"
            }
    
    def _execute_echo(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implementation of echo tool.
        
        Args:
            arguments: Must contain 'message'
            
        Returns:
            Echo result
        """
        message = arguments.get("message", "")
        return {
            "status": "success",
            "result": f"Echo: {message}"
        }
    
    def _execute_process_data(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implementation of process_data tool.
        
        Args:
            arguments: Must contain 'data' and 'operation'
            
        Returns:
            Processed data result
        """
        data = arguments.get("data", "")
        operation = arguments.get("operation", "uppercase")
        
        try:
            if operation == "uppercase":
                result = data.upper()
            elif operation == "lowercase":
                result = data.lower()
            elif operation == "reverse":
                result = data[::-1]
            else:
                return {"status": "error", "message": "Invalid operation"}
            
            return {
                "status": "success",
                "operation": operation,
                "result": result
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Processing failed: {str(e)}"
            }
    
    def initialize(self) -> bool:
        """
        Initialize the server.
        
        Returns:
            True if initialization successful
        """
        try:
            self.define_tools()
            self.initialized = True
            logger.info(f"{self.server_name} initialized with {len(self.tools)} tools")
            return True
        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            return False
    
    def shutdown(self) -> None:
        """
        Shutdown the server gracefully.
        """
        logger.info(f"Shutting down {self.server_name}")
        self.initialized = False


# Example usage
if __name__ == "__main__":
    # Create server instance
    server = MCPServerTemplate("MyTemplateServer")
    
    # Initialize
    if server.initialize():
        print("\n" + "="*50)
        print("MCP SERVER TEMPLATE - DEMONSTRATION")
        print("="*50)
        
        # List available tools
        print("\n📋 Available Tools:")
        for tool in server.get_tools():
            print(f"  - {tool['name']}: {tool['description']}")
        
        # Test Tool 1: Echo
        print("\n🧪 Test 1: Echo Tool")
        result = server.execute_tool("echo", {"message": "Hello, MCP!"})
        print(f"  Result: {json.dumps(result, indent=2)}")
        
        # Test Tool 2: Process Data
        print("\n🧪 Test 2: Process Data Tool")
        result = server.execute_tool(
            "process_data",
            {"data": "hello world", "operation": "uppercase"}
        )
        print(f"  Result: {json.dumps(result, indent=2)}")
        
        # Cleanup
        server.shutdown()
        print("\n✅ Demo completed successfully!\n")
