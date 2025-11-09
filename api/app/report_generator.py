from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# Set up Jinja2 environment to load templates from the folder
template_dir = Path(__file__).parent / "report_templates"
env = Environment(loader=FileSystemLoader(template_dir))

def generate_executive_report(dashboard_data: dict) -> str:
    """Renders the executive report HTML using dashboard analytics data."""
    template = env.get_template("executive.html")
    
    # Render the template with the data
    html_output = template.render(
        report_title="Project GRC-MMAP Executive Summary",
        generation_date=dashboard_data['finding_trend'][-1]['date'] if dashboard_data['finding_trend'] else 'N/A',
        data=dashboard_data
    )
    return html_output