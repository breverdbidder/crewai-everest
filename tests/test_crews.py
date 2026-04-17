"""Smoke tests — crews build without errors."""
import pytest


def test_zonewise_crew_builds():
    from everest_config.crews.zonewise import build_zonewise_crew
    crew = build_zonewise_crew()
    assert len(crew.agents) == 3
    assert len(crew.tasks) == 3
    roles = [a.role for a in crew.agents]
    assert "FL Zoning Data Researcher" in roles
    assert "Zoning Compliance Analyst" in roles
    assert "Buyer-Facing Zoning Report Writer" in roles


def test_tenants_yaml_complete():
    import yaml
    from pathlib import Path

    path = Path(__file__).parent.parent / "everest_config" / "tenants.yaml"
    assert path.exists()
    data = yaml.safe_load(path.read_text())
    tenant_slugs = set(data["tenants"].keys())
    expected = {"biddeed", "zonewise", "property360", "kenstrekt",
                "protection-partners", "everest-capital", "everest-portfolio", "brevard-doors"}
    assert tenant_slugs == expected, f"Mismatch: {tenant_slugs ^ expected}"
