from base64 import b64encode

from riddle.urls import add_route

from . import success_message

encrypted_url = '/oaZtyvM5wVdOBplOHhgI3OvVdk6NVaurhAybOaSGycOE93CXiJOf4KwrNB7rJBbL4rk2bLHuLOjzHeqLF3mVXwXtxC4teqWr2igS'

@add_route(encrypted_url, endpoint="wasp9_message")
def entry():
    return {
        'content': b64encode(success_message.encode()).decode(),
        'answer': 'pass',  # Solved as soon as it is opened
    }