from jinja2 import Template
import pdfkit


def print_comments(data):
    template = Template('Hello {{ name }}!')
    html = template.render(name='John Doe')
    pdfkit.from_string(html, "/Users/akd/Desktop/1.pdf", options={"zoom": 8})
    return "/Users/akd/Desktop/1.pdf"
