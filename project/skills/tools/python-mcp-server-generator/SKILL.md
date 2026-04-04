---
name: python-mcp-server-generator
description: Generate Python MCP Server - Create a complete Model Context Protocol (MCP) server in Python with proper structure, type hints, and error handling.
version: 1.0.0
author: github/awesome-copilot
tags:
  - python
  - mcp
  - server
  - generator
  - llm
  - claude
---

# Generate Python MCP Server

Create a complete Model Context Protocol (MCP) server in Python with the following specifications:

## Requirements

- **Project Structure**: Create a new Python project with proper structure using uv
- **Dependencies**: Include mcp[cli] package with uv
- **Transport Type**: Choose between stdio (for local) or streamable-http (for remote)
- **Tools**: Create at least one useful tool with proper type hints
- **Error Handling**: Include comprehensive error handling and validation

## Implementation Details

### Project Setup

1. Initialize with `uv init project-name`
2. Add MCP SDK: `uv add "mcp[cli]"`
3. Create main server file (e.g., `server.py`)
4. Add `.gitignore` for Python projects
5. Configure for direct execution with `if __name__ == "__main__"`

### Server Configuration

- Use `FastMCP` class from `mcp.server.fastmcp`
- Set server name and optional instructions
- Choose transport: `stdio` (default) or `streamable-http`
- For HTTP: optionally configure host, port, and stateless mode

### Tool Implementation

- Use `@mcp.tool()` decorator on functions
- Always include type hints - they generate schemas automatically
- Write clear docstrings - they become tool descriptions
- Use Pydantic models or TypedDicts for structured outputs
- Support async operations for I/O-bound tasks
- Include proper error handling

### Resource/Prompt Setup (Optional)

- Add resources with `@mcp.resource()` decorator
- Use URI templates for dynamic resources: `"resource://{param}"`
- Add prompts with `@mcp.prompt()` decorator
- Return strings or Message lists from prompts

### Code Quality

- Use type hints for all function parameters and returns
- Write docstrings for tools, resources, and prompts
- Follow PEP 8 style guidelines
- Use async/await for asynchronous operations
- Implement context managers for resource cleanup
- Add inline comments for complex logic

## Example Tool Types to Consider

- Data processing and transformation
- File system operations (read, analyze, search)
- External API integrations
- Database queries
- Text analysis or generation (with sampling)
- System information retrieval
- Math or scientific calculations

## Configuration Options

### For stdio Servers

```python
# Simple direct execution
# Test with: uv run mcp dev server.py
# Install to Claude: uv run mcp install server.py
```

### For HTTP Servers

```python
# Port configuration via environment variables
# Stateless mode for scalability: stateless_http=True
# JSON response mode: json_response=True
# CORS configuration for browser clients
# Mounting to existing ASGI servers (Starlette/FastAPI)
```

## Testing Guidance

Explain how to run the server:

- **stdio**: `python server.py` or `uv run server.py`
- **HTTP**: `python server.py` then connect to `http://localhost:PORT/mcp`
- Test with MCP Inspector: `uv run mcp dev server.py`
- Install to Claude Desktop: `uv run mcp install server.py`
- Include example tool invocations
- Add troubleshooting tips

## Additional Features to Consider

- **Context usage**: for logging, progress, and notifications
- **LLM sampling**: for AI-powered tools
- **User input elicitation**: for interactive workflows
- **Lifespan management**: for shared resources (databases, connections)
- **Structured output**: with Pydantic models
- **Icons**: for UI display
- **Image handling**: with Image class
- **Completion support**: for better UX

## Best Practices

1. **Use type hints everywhere** - they're not optional
2. **Return structured data** when possible
3. **Log to stderr** (or use Context logging) to avoid stdout pollution
4. **Clean up resources** properly
5. **Validate inputs** early
6. **Provide clear error messages**
7. **Test tools independently** before LLM integration

## Example Implementation

```python
# server.py
from mcp.server.fastmcp import FastMCP

# Create server instance
mcp = FastMCP(
    name="my-server",
    instructions="A sample MCP server"
)

# Define a tool
@mcp.tool()
async def hello(name: str) -> str:
    """Say hello to someone.
    
    Args:
        name: The name of the person to greet
        
    Returns:
        A greeting message
    """
    return f"Hello, {name}!"

# Run the server
if __name__ == "__main__":
    mcp.run()
```

## Project Structure Template

```
my-mcp-server/
├── .gitignore
├── pyproject.toml
├── README.md
├── src/
│   └── my_server/
│       ├── __init__.py
│       ├── server.py
│       └── tools/
│           ├── __init__.py
│           └── example.py
└── tests/
    └── test_server.py
```

---

Generate a complete, production-ready MCP server with type safety, proper error handling, and comprehensive documentation.
