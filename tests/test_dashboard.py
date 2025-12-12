import types
import src.frontend.dashboard as dashboard


def test_dashboard_module_imports():
    """Dashboard module should import without errors."""
    assert isinstance(dashboard, types.ModuleType)
