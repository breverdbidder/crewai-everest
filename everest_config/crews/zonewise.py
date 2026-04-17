"""ZoneWise.AI Crew — zoning intelligence across 67 FL counties.

Canonical pattern for all 8 Everest tenants. Replaces planned kortix-ai/suna usage.
"""
from __future__ import annotations

from crewai import Agent, Crew, Process, Task


def build_zonewise_crew() -> Crew:
    """Build ZoneWise Crew: Researcher + Analyst + Writer."""
    researcher = Agent(
        role="FL Zoning Data Researcher",
        goal="Pull authoritative zoning, FLU, overlay data for a parcel from zw_parcels (77 cols SSOT).",
        backstory=(
            "Senior research agent trained on 67 FL county zoning regulations. "
            "Cross-references parcel boundaries with FEMA flood maps, FDEP CCCL lines, "
            "and municipal FLU overlays. Never fabricates data; if a field is missing, "
            "says 'unknown — needs county sync'."
        ),
        allow_delegation=False,
        verbose=False,
    )
    analyst = Agent(
        role="Zoning Compliance Analyst",
        goal="Translate raw zoning codes into buildable/non-buildable verdicts + risk flags.",
        backstory=(
            "Land-use law background. Thinks in terms of 'what can actually be built here'. "
            "Cites specific code sections. Never hand-waves 'should be OK'."
        ),
        allow_delegation=False,
        verbose=False,
    )
    writer = Agent(
        role="Buyer-Facing Zoning Report Writer",
        goal="Turn findings into a concise buyer report: allowed, risky, unknown.",
        backstory=(
            "Writes for sophisticated real estate investors. Leads with actionable "
            "answer, then shows work. BrandGuard tone: direct, no softening."
        ),
        allow_delegation=False,
        verbose=False,
    )

    research_task = Task(
        description="Pull zoning, FLU, overlays, flood zone, CCCL status for parcel {parcel_id}.",
        expected_output="YAML with zoning_code, flu_code, overlays[], flood_zone, cccl_status, data_gaps[].",
        agent=researcher,
    )
    analysis_task = Task(
        description="Produce use-case verdict: primary allowed uses, height/setback constraints, risks.",
        expected_output="YAML with allowed_uses[], constraints{}, risks[], confidence.",
        agent=analyst,
        context=[research_task],
    )
    writing_task = Task(
        description="Produce 1-page buyer brief: BUILDABLE/CONDITIONAL/NON-BUILDABLE verdict + envelope + risks.",
        expected_output="Markdown buyer brief, <500 words.",
        agent=writer,
        context=[research_task, analysis_task],
    )

    return Crew(
        agents=[researcher, analyst, writer],
        tasks=[research_task, analysis_task, writing_task],
        process=Process.sequential,
        verbose=False,
    )


if __name__ == "__main__":
    crew = build_zonewise_crew()
    print(f"[OK] ZoneWise Crew built: {len(crew.agents)} agents, {len(crew.tasks)} tasks")
