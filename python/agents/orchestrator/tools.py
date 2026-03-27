from typing import Optional, Dict, Any


def say_hello(name: Optional[str] = None) -> str:
    """Provides a simple greeting. If a name is provided, it will be used.

    Args:
        name (str, optional): The name of the person to greet.
    """
    if name:
        return f"Hello, {name}!"
    return "Hello there!"


def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    return "Goodbye! Have a great day."


def render_ui(
    component_type: str, data: Dict[str, Any], title: Optional[str] = None
) -> str:
    """Renders a structured UI component for the user (A2UI protocol).
    Use this for charts, tables, approval forms, or complex data visualizations.

    Args:
        component_type: The type of UI component (e.g., 'chart', 'table', 'form', 'card').
        data: The JSON data required by the component.
        title: Optional title for the UI component.
    """
    # In a real implementation, this would return metadata or a specific object
    # that the AG-UI streaming layer would intercept and render as a widget.
    return f"[A2UI: {component_type}] {title or ''} - Data: {data}"
