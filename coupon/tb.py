import json
import random

from coupon.delivery import find_group_usernames, send_image, send_text
from coupon.pricing import format_price
from untils.retry import retry_call


def tb_share_text(group_name: str, material_id: str, app_key, app_secret, adzone_id):
    client = create_taobao_client(app_key, app_secret, adzone_id)
    selected_material_id = choose_material_id(material_id)
    print(selected_material_id)

    def fetch_goods():
        res = client.taobao_tbk_dg_optimus_material(selected_material_id)
        return json.loads(res)["tbk_dg_optimus_material_response"]["result_list"]["map_data"]

    goods_list = retry_call("taobao material query", fetch_goods)
    for room_name in find_group_usernames(group_name):
        for item in goods_list:
            send_taobao_item(room_name, client, item)


def choose_material_id(material_id):
    material_ids = [item.strip() for item in str(material_id).split(",") if item.strip()]
    if not material_ids:
        raise ValueError("material_id cannot be empty")
    return str(random.choice(material_ids))


def send_taobao_item(room_name, client, item):
    image_url = "https:" + str(item["pict_url"])
    token = create_tpwd(client, item["title"], get_share_url(item))

    send_image(room_name, image_url, item["item_id"], 1, 5)
    send_text(room_name, build_taobao_text(item), 2, 2)
    send_text(room_name, "({})".format(token), 1, 3)


def build_taobao_text(item):
    final_price = float(item["zk_final_price"])
    coupon_amount = float(item.get("coupon_amount", 0) or 0)
    return "{}\n{}\n{}".format(
        item["title"],
        "\u3010\u5728\u552e\u4ef7\u3011\u00a5{}".format(format_price(final_price)),
        "\u3010\u5238\u540e\u4ef7\u3011\u00a5{}".format(format_price(final_price - coupon_amount)),
    )


def get_share_url(item):
    if item.get("coupon_share_url"):
        return "https:" + item["coupon_share_url"]
    return "https:" + item["click_url"]


def create_tpwd(client, title, share_url):
    text = str(client.taobao_tbk_tpwd_create(title, share_url))
    start_index = find_tpwd_start(text)
    if start_index == -1:
        return text
    return text[start_index: 13 + start_index]


def find_tpwd_start(text):
    indexes = [text.find(symbol) for symbol in ("\uffe5", "\u00a5", "?") if text.find(symbol) != -1]
    return min(indexes) if indexes else -1


def create_taobao_client(app_key, app_secret, adzone_id):
    from untils.tb_top_api import TbApiClient

    return TbApiClient(app_key=app_key, secret_key=app_secret, adzone_id=adzone_id)


if __name__ == '__main__':
    print("tb function")
