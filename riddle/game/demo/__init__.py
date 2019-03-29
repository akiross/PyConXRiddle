from jinja2 import Environment, DictLoader

base_html = '''<!doctype html>
<html>
<head><title>Hello there!</title></head>
<body>
{% block body %}{% endblock %}
</body>
</html>
'''

env = Environment(
        loader=DictLoader({'base': base_html})
)
