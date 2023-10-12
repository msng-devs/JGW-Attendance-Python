# TODO: 출결 기한이 만료된 경우, ACK로 출석을 하지 않은 유저들의 출석 정보를 ABS로 업데이트.
# TODO: 기한이 만료된 출석 정보를 업데이트하는 로직 작성.
# --------------------------------------------------------------------------
# Scheduling을 위한 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------

import json
import zmq

from django.conf import settings


def send_mail(to: str, subject: str, template: str, args: str, service_name: str):
    """
    zmq를 통해 메일을 발송합니다.

    :param to: 메일을 받을 사람의 이메일 주소입니다.
    :param subject: 메일 제목입니다.
    :param template: 메일 내용입니다.
    :param args: 메일 내용에 들어갈 인자입니다.
    :param service_name: 메일을 발송하는 서비스의 이름입니다.
    :return: None
    """
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
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
