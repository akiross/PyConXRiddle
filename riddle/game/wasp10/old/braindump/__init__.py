list_page = """
<!doctype html>
<html>
<body>
    <h1>Content of {{directory}}</h1>
    <ul>
    {% for url, name in directories %}
        <li style='list-style-type: "\\1F4C1"'><a href="{{url}}">{{name}}</a></li>
    {% endfor %}
    {% for url, name in resources %}
        <li style='list-style-type: "\\1F5B9"'><a href="/{{url}}">{{name}}</a></li>
    {% endfor %}
    </ul>
</body>
</html>
"""
