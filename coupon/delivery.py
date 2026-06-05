# coding=utf-8
import random
import time

from untils.common import del_pic, save_pic

_chat_client = None


def get_chat_client():
    global _chat_client
    if _chat_client is not None:
        return _chat_client

    import itchat

    _chat_client = itchat
    return _chat_client


def find_group_usernames(group_name):
    groups = get_chat_client().search_chatrooms(name=str(group_name)) or []
    return [group["UserName"] for group in groups]


def wait_random(min_seconds=1, max_seconds=3):
    time.sleep(random.randint(min_seconds, max_seconds))


def send_text(room_name, text, min_delay=1, max_delay=3):
    wait_random(min_delay, max_delay)
    send_message(room_name, text)


def send_group_text(group_name, text, min_delay=1, max_delay=3):
    for room_name in find_group_usernames(group_name):
        send_text(room_name, text, min_delay, max_delay)


def send_image(room_name, image_url, item_id, min_delay=1, max_delay=3):
    filename = None
    try:
        wait_random(min_delay, max_delay)
        filename = save_pic(image_url, item_id)
        if filename:
            send_message(room_name, '@img@%s' % filename)
    finally:
        del_pic(filename)


def send_group_image(group_name, image_url, item_id, min_delay=1, max_delay=3):
    for room_name in find_group_usernames(group_name):
        send_image(room_name, image_url, item_id, min_delay, max_delay)


def send_group_image_text(group_name, image_url, item_id, text):
    for room_name in find_group_usernames(group_name):
        send_image(room_name, image_url, item_id, 1, 5)
        send_text(room_name, text, 1, 3)


def send_message(room_name, text):
    get_chat_client().send(text, room_name)
