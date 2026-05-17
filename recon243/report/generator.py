from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from rich.console import Console

console = Console()

class HTMLReportGenerator:
    def __init__(self, data):
        self.data = data
        self.template_dir = Path(__file__).parent.parent.parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
    
    def generate(self, output_path):
        template = self.env.get_template("report.html")
        html_content = template.render(data=self.data)
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        console.print(f"✨ HTML report generated: {output_path}")
