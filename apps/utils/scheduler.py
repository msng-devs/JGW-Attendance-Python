import json
import zmq

from django.conf import settings


def send_mail(to: str, subject: str, template: str, args: str, service_name: str):
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    print("PUSH Socket Connected at:", settings.ZMQ_PORT)
    zmq_socket.connect(f"tcp://{settings.ZMQ_HOST}:{settings.ZMQ_PORT}")

    message = {
        "to": to,
        "subject": subject,
        "template": template,
        "arg": args,
        "who": service_name,
    }
    request = json.dumps(
        message,
        default=lambda o: o.__dict__,
        sort_keys=True,
        indent=4,
        ensure_ascii=False,
    )
    zmq_socket.send_json(request)
    print("Message Sent to PULL Socket:", request)
