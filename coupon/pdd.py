import json
import random

from coupon.delivery import send_group_image_text
from coupon.pricing import clamp_min, format_fen
from untils.retry import retry_call


def pdd_share_text(group_name: str, group_material_id: str, app_key: str, secret_key: str, p_id: str):
    def fetch_goods():
        offset = str(random.randint(1, 295))
        limit = str(random.randint(3, 5))
        client = create_pdd_client(app_key, secret_key)
        return client.call(
            "pdd.ddk.top.goods.list.query",
            {
                "offset": offset,
                "limit": limit,
                "p_id": p_id,
            },
        )

    def notice_error(exception, attempt):
        send_system_notice("pinduoduo attempt: {}\n{}".format(attempt, exception))

    resp = retry_call("pinduoduo goods query", fetch_goods, on_error=notice_error)
    goods_list = json.loads(resp.text)["top_goods_list_get_response"]["list"]

    for data in goods_list:
        short_url = promotion_url_generate(
            app_key=app_key,
            secret_key=secret_key,
            p_id=p_id,
            goods_id_list=int(data["goods_id"]),
            search_id=data["search_id"],
        )
        send_group_image_text(
            group_name,
            data["goods_thumbnail_url"],
            data["goods_id"],
            build_pdd_text(data, short_url),
        )


def build_pdd_text(data, short_url):
    base_price = min(int(data["min_group_price"]), int(data["min_normal_price"]))
    coupon_price = clamp_min(base_price - int(data["coupon_discount"]))
    return " {}\n{}\n{}\n-----------------\n{}:\n{}".format(
        data["goods_name"],
        "\u3010\u73b0\u4ef7\u3011\u00a5{}".format(format_fen(base_price)),
        "\u3010\u5185\u90e8\u4ef7\u3011\u00a5{}".format(format_fen(coupon_price)),
        "\u62a2\u8d2d\u5730\u5740",
        short_url,
    )


def promotion_url_generate(app_key: str, secret_key: str, p_id: str, goods_id_list: int, search_id: str):
    client = create_pdd_client(app_key, secret_key)
    resp = client.call(
        "pdd.ddk.goods.promotion.url.generate",
        {
            "goods_id_list": "[{}]".format(goods_id_list),
            "search_id": search_id,
            "p_id": p_id,
        },
    )
    try:
        return json.loads(resp.text)["goods_promotion_url_generate_response"]["goods_promotion_url_list"][0][
            "mobile_short_url"
        ]
    except Exception as exception:
        print(exception)
        send_system_notice(
            "goods_id_list: {}\nsearch_id: {}\np_id: {}\n\nCannot get promotion url".format(
                goods_id_list,
                search_id,
                p_id,
            )
        )
        return ""


def send_system_notice(text):
    from chat.itchatHelper import set_system_notice

    set_system_notice(text)


def create_pdd_client(app_key, secret_key):
    from untils.pdd_api import PddApiClient

    return PddApiClient(app_key=app_key, secret_key=secret_key)
