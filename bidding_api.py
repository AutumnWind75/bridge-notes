import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


HOST = os.getenv("BIDDING_API_HOST", "127.0.0.1")
PORT = int(os.getenv("BIDDING_API_PORT", "8000"))

SUIT_NAMES = {
    "C": "梅花",
    "D": "方块",
    "H": "红心",
    "S": "黑桃",
    "NT": "无将",
}


OPENING_EXPLANATIONS = {
    "1C": "12-21 点，至少 3 张梅花。",
    "1D": "12-21 点，4 张方片（仅 4432 牌型允许 3 张方片）。",
    "1H": "12-21 点，至少 5 张红心。",
    "1S": "12-21 点，至少 5 张黑桃。",
    "1NT": "15-17 点均型，可能有 5 张高花或 6 张低花。",
    "2NT": "20-21 点均型，可能有 5 张高花或 6 张低花。",
    "2C": "22 点以上任意牌型。",
    "2D": "6-10 点，至少 6 张方片，阻击叫。",
    "2H": "6-10 点，至少 6 张红心，阻击叫。",
    "2S": "6-10 点，至少 6 张黑桃，阻击叫。",
}


RESPONSE_EXPLANATIONS = {
    "1C": {
        "1D": "6 点以上，至少 4 张方片，否认 4 张高花。",
        "1H": "6 点以上，至少 4 张红心。",
        "1S": "6 点以上，至少 4 张黑桃。",
        "1NT": "均型，否认 4 张高花；6-10 点。",
        "2NT": "均型，否认 4 张高花；11-12 点，邀请。",
        "3NT": "均型，否认 4 张高花；13-15 点，直接进局。",
        "2C": "11 点以上，至少 5 张梅花支持，逼叫一轮。",
        "2D": "4-6 点，至少 6 张方片，弱跳叫，不逼叫。",
        "2H": "4-6 点，至少 6 张红心，弱跳叫，不逼叫。",
        "2S": "4-6 点，至少 6 张黑桃，弱跳叫，不逼叫。",
        "3C": "5-7 点，至少 5 张梅花支持，阻击叫。",
        "3D": "11 点以上，至少 4 张梅花支持，方片单缺，无 4 张高花，Splinter。",
        "3H": "11 点以上，至少 4 张梅花支持，红心单缺，无 4 张高花，Splinter。",
        "3S": "11 点以上，至少 4 张梅花支持，黑桃单缺，无 4 张高花，Splinter。",
    },
    "1D": {
        "1H": "6 点以上，至少 4 张红心。",
        "1S": "6 点以上，至少 4 张黑桃。",
        "1NT": "均型，否认 4 张高花；6-10 点。",
        "2NT": "均型，否认 4 张高花；11-12 点，邀请。",
        "3NT": "均型，否认 4 张高花；13-15 点，直接进局。",
        "2C": "13 点以上，至少 5 张梅花（通常非均型），否认 4 张高花，二盖一逼局。",
        "2D": "11 点以上，至少 5 张方片支持，逼叫一轮。",
        "2H": "4-6 点，至少 6 张红心，弱跳叫，不逼叫。",
        "2S": "4-6 点，至少 6 张黑桃，弱跳叫，不逼叫。",
        "3C": "9-11 点，至少 6 张梅花，建设性阻击。",
        "3D": "5-7 点，至少 5 张方片支持，阻击叫。",
        "3H": "11 点以上，至少 4 张方片支持，红心单缺，无 4 张高花，Splinter。",
        "3S": "11 点以上，至少 4 张方片支持，黑桃单缺，无 4 张高花，Splinter。",
    },
    "1H": {
        "1S": "6 点以上，至少 4 张黑桃，逼叫一轮。",
        "1NT": "6-12 点，均型牌，否认 3 张红心支持；否认 4 张黑桃",
        "2C": "13 点以上，至少 3 张梅花，二盖一逼局。",
        "2D": "13 点以上，至少 3 张方片，二盖一逼局。",
        "2H": "7-10 点，至少 3 张红心支持，建设性邀请。",
        "2NT": "13 点以上，至少 4 张红心支持，Jacoby 2NT，逼局。",
        "3C": "4-6 点，6 张梅花，弱跳叫，不逼叫。",
        "3D": "4-6 点，6 张方片，弱跳叫，不逼叫。",
        "3H": "5-7 点，通常至少 4 张红心支持，阻击叫，不逼叫。",
        "3S": "10-12 点，至少 4 张红心支持，有一门单缺，Mini-Splinter。",
        "3NT": "13-15 点，至少 4 张红心支持，黑桃单缺，Splinter。",
        "4C": "13-15 点，至少 4 张红心支持，梅花单缺，Splinter。",
        "4D": "13-15 点，至少 4 张红心支持，方片单缺，Splinter。",
        "4H": "有 5 张以上红心支持，直接进局止叫，限制性牌力。",
    },
    "1S": {
        "1NT": "6-12 点，均型牌，否认 3 张黑桃支持。",
        "2C": "13 点以上，至少 3 张梅花，二盖一逼局。",
        "2D": "13 点以上，至少 3 张方片，二盖一逼局。",
        "2H": "13 点以上，至少 5 张红心，二盖一逼局。",
        "2S": "7-10 点，至少 3 张黑桃支持，建设性邀请。",
        "2NT": "13 点以上，至少 4 张黑桃支持，Jacoby 2NT，逼局。",
        "3C": "4-6 点，6 张梅花，弱跳叫，不逼叫。",
        "3D": "4-6 点，6 张方片，弱跳叫，不逼叫。",
        "3H": "10-12 点，至少 4 张黑桃支持，有一门单缺，Mini-Splinter。",
        "3S": "5-7 点，通常至少 4 张黑桃支持，阻击叫，不逼叫。",
        "3NT": "13-15 点，至少 4 张黑桃支持，红心单缺，Splinter。",
        "4C": "13-15 点，至少 4 张黑桃支持，梅花单缺，Splinter。",
        "4D": "13-15 点，至少 4 张黑桃支持，方片单缺，Splinter。",
        "4S": "有 5 张以上黑桃支持，直接进局止叫，限制性牌力。",
    },
    "1NT": {
        "2C": "8 点以上，至少有一门 4 张高花，斯台曼，寻找 4-4 高花配合。",
        "2D": "至少 5 张红心，Jacoby 转移叫。",
        "2H": "至少 5 张黑桃，Jacoby 转移叫。",
        "2S": "低花转移叫，要求开叫人叫 3C。",
        "2NT": "8-9 点，均型牌，无 4 张高花，自然邀请。",
        "3C": "8-9 点，至少 6 张梅花，低花邀请。",
        "3D": "8-9 点，至少 6 张方片，低花邀请。",
        "3H": "通常至少 5-4 双低花，逼局，红心单缺。",
        "3S": "通常至少 5-4 双低花，逼局，黑桃单缺。",
        "4C": "Gerber，询问开叫人有几个 A。",
        "4D": "Texas 转移叫，至少 6 张红心，直接进局止叫。",
        "4H": "Texas 转移叫，至少 6 张黑桃，直接进局止叫。",
        "4NT": "16-17 点，均型牌，示量邀请 6NT。",
        "4S": "6 张梅花和 5 张方片，低花选局。",
    },
    "2NT": {
        "3C": "Puppet Stayman，寻找 4 张或 5 张高花。",
        "3D": "至少 5 张红心，转移叫。",
        "3H": "至少 5 张黑桃，转移叫。",
        "3S": "低花 Stayman，寻找 4-4 低花配合，通常有满贯兴趣。",
        "4C": "Gerber，询问开叫人有几个 A。",
        "4D": "Texas 转移叫，至少 6 张红心，直接进局止叫。",
        "4H": "Texas 转移叫，至少 6 张黑桃，直接进局止叫。",
        "4NT": "11-12 点，均型牌，示量邀请 6NT。",
    },
}


def first_competitive_explanations(auction, dealer="N", seat="S"):
    """Return chapter six meanings when partner has not entered the auction."""
    if not isinstance(auction, list) or seat not in ("N", "E", "S", "W"):
        return {}

    seats = ["W", "N", "E", "S"]
    if dealer not in seats or not auction:
        return {}

    current_index = (seats.index(dealer) + len(auction) - 1) % 4
    if seats[current_index] != seat:
        return {}

    partner = {"N": "S", "S": "N", "E": "W", "W": "E"}[seat]
    partner_has_action = any(
        bid not in ("Pass", "P")
        and seats[(seats.index(dealer) + index) % 4] == partner
        for index, bid in enumerate(auction[:-1])
    )
    if partner_has_action:
        return {}

    opening_index = next(
        (
            index for index, bid in enumerate(auction)
            if _bid_level(bid) == 1 and _bid_suit(bid) is not None
        ),
        None,
    )
    if opening_index is None:
        return {}

    opening_bid = auction[opening_index]
    opening_suit = _bid_suit(opening_bid)
    if seats[(seats.index(dealer) + opening_index) % 4] in (seat, partner):
        return {}

    all_suits = ("C", "D", "H", "S")
    unbid_suits = [suit for suit in all_suits if suit != opening_suit]
    higher_suits = [suit for suit in unbid_suits if all_suits.index(suit) > all_suits.index(opening_suit)]
    lower_suits = [suit for suit in unbid_suits if all_suits.index(suit) < all_suits.index(opening_suit)]
    position = (len(auction) - 1) % 4
    explanations = {}
    explanations["X"] = "12+ 点，其他套都有 3+ 张支持；或 17+ 点加倍出套；或 19+ 点任意牌型。"

    if position == 1:
        explanations["1NT"] = "15-18 点，均型。"
    elif position == 3:
        explanations["1NT"] = "12-15 点，均型；后续应叫同开叫 1NT。"

    if higher_suits:
        for suit in higher_suits:
            explanations[f"1{suit}"] = "5 张以上套，8-16 点。"
    if lower_suits:
        for suit in lower_suits:
            explanations[f"2{suit}"] = "5 张以上套，11-16 点。"

    if opening_suit in ("C", "D"):
        explanations[f"2{opening_suit}"] = "迈克尔斯扣叫：至少 5-5 双高花，8 点以上，点集中在长套上。"
    else:
        explanations[f"2{opening_suit}"] = "迈克尔斯扣叫：5-5 另一高花和任一低花，10 点以上，点集中在长套上。"

    if position == 1:
        explanations["2NT"] = "最低级别的两个未叫套。"
    elif position == 3:
        explanations["2NT"] = "19-20 点，均型；后续 3C 为 Stayman。"

    for level in range(3, 8):
        if higher_suits:
            for suit in higher_suits:
                explanations[f"{level}{suit}"] = "阻击叫。"
        if lower_suits:
            for suit in lower_suits:
                explanations[f"{level}{suit}"] = "阻击叫。"
        explanations[f"{level}{opening_suit}"] = "有一低花坚固套，或是高花套不适合加倍的畸形牌。"

    return explanations


def convention_explanations(auction, dealer="N", seat="S"):
    """Return follow-up explanations for conventions described in the chapters."""
    if not isinstance(auction, list):
        return {}

    calls = [bid for bid in auction if bid not in ("Pass", "P")]
    explanations = {}
    explanations.update(first_competitive_explanations(auction, dealer, seat))

    def contains_sequence(sequence):
        size = len(sequence)
        return any(calls[index:index + size] == sequence for index in range(len(calls)))

    if "1H" in calls and "2NT" in calls:
        explanations.update({
            "3C": "所叫花色为单缺。",
            "3D": "所叫花色为单缺。",
            "3H": "16 点以上，无单缺。",
            "3NT": "14-15 点，无单缺。",
            "4C": "所叫花色至少 5 张，且至少 KQ 领头。",
            "4D": "所叫花色至少 5 张，且至少 KQ 领头。",
            "4H": "低限，无单缺，3 控以下。",
        })
    elif "1S" in calls and "2NT" in calls:
        explanations.update({
            "3C": "所叫花色为单缺。",
            "3D": "所叫花色为单缺。",
            "3H": "所叫花色为单缺。",
            "3S": "16 点以上，无单缺。",
            "3NT": "14-15 点，无单缺。",
            "4C": "所叫花色至少 5 张，且至少 KQ 领头。",
            "4D": "所叫花色至少 5 张，且至少 KQ 领头。",
            "4H": "所叫花色至少 5 张，且至少 KQ 领头。",
            "4S": "低限，无单缺，3 控以下。",
        })

    if contains_sequence(["1NT", "2C"]):
        explanations.update({
            "2D": "否认 4 张高花。",
            "2H": "有 4 张红心，可能同时有 4 张黑桃。",
            "2S": "有 4 张黑桃，否认 4 张红心。",
        })
    if contains_sequence(["1NT", "2D"]):
        explanations["2H"] = "开叫人必须叫 2H，完成红心转移。"
    if contains_sequence(["1NT", "2H"]):
        explanations["2S"] = "开叫人必须叫 2S，完成黑桃转移。"
    if contains_sequence(["1NT", "2S", "3C"]):
        explanations.update({
            "Pass": "单套弱低花，通常是长梅花，不想打 1NT。",
            "3D": "双套弱低花，至少 5-5，让开叫人在 3D 和 3C 中选择。",
            "3H": "双低花逼局牌，红心单缺，有满贯兴趣。",
            "3S": "双低花逼局牌，黑桃单缺，有满贯兴趣。",
        })
    if contains_sequence(["1NT", "4C"]):
        explanations.update({
            "4D": "0 或 4 个 A。",
            "4H": "1 个 A。",
            "4S": "2 个 A。",
            "4NT": "3 个 A。",
        })
    if contains_sequence(["1NT", "4D"]):
        explanations["4H"] = "开叫人必须叫 4H，完成红心 Texas 转移。"
    if contains_sequence(["1NT", "4H"]):
        explanations["4S"] = "开叫人必须叫 4S，完成黑桃 Texas 转移。"

    if contains_sequence(["2NT", "3C"]):
        explanations.update({
            "3D": "否认有 4 张或 5 张高花。",
            "3H": "有 5 张红心。",
            "3S": "有 5 张黑桃。",
            "3NT": "有 4 张红心和 4 张黑桃，双高花。",
        })
    if contains_sequence(["2NT", "3D"]):
        explanations["3H"] = "开叫人必须叫 3H，完成红心转移。"
    if contains_sequence(["2NT", "3H"]):
        explanations["3S"] = "开叫人必须叫 3S，完成黑桃转移。"
    if contains_sequence(["2NT", "3S"]):
        explanations.update({
            "3NT": "否认有 4 张低花。",
            "4C": "有 4 张梅花。",
            "4D": "有 4 张方片。",
        })
    if contains_sequence(["2NT", "4C"]):
        explanations.update({
            "4D": "0 或 4 个 A。",
            "4H": "1 个 A。",
            "4S": "2 个 A。",
            "4NT": "3 个 A。",
        })
    if contains_sequence(["2NT", "4D"]):
        explanations["4H"] = "开叫人必须叫 4H，完成红心 Texas 转移。"
    if contains_sequence(["2NT", "4H"]):
        explanations["4S"] = "开叫人必须叫 4S，完成黑桃 Texas 转移。"

    if contains_sequence(["1H", "3S", "3NT"]):
        explanations.update({
            "4C": "回答单缺：梅花单缺。",
            "4D": "回答单缺：方片单缺。",
            "4H": "回答单缺：黑桃单缺。",
        })
    elif contains_sequence(["1S", "3H", "3S"]):
        explanations.update({
            "3NT": "回答单缺：红心单缺。",
            "4C": "回答单缺：梅花单缺。",
            "4D": "回答单缺：方片单缺。",
        })

    return explanations


def _bid_suit(bid):
    if not isinstance(bid, str) or bid.endswith("NT"):
        return None
    return bid[-1] if bid[-1] in ("C", "D", "H", "S") else None


def _bid_level(bid):
    if not isinstance(bid, str) or not bid[:1].isdigit():
        return None
    return int(bid[0])


def _keycard_trump(auction, ask_index):
    suits_by_side = {0: set(), 1: set()}
    for index, bid in enumerate(auction[:ask_index + 1]):
        suit = _bid_suit(bid)
        if suit:
            suits_by_side[index % 2].add(suit)
            if suit in suits_by_side[1 - (index % 2)]:
                return suit

    for bid in reversed(auction[:ask_index]):
        suit = _bid_suit(bid)
        if suit:
            return suit
    return None


def _next_bid_after(bid):
    level = _bid_level(bid)
    suit = _bid_suit(bid)
    if level is None:
        return None
    if suit is None:
        return f"{level + 1}C"

    suit_order = ("C", "D", "H", "S")
    suit_index = suit_order.index(suit)
    if suit_index == len(suit_order) - 1:
        return f"{level}NT"
    return f"{level}{suit_order[suit_index + 1]}"


def _keycard_response_meaning(bid, trump, interfered):
    if not interfered:
        return {
            "5C": "1 或 4 个关键张。",
            "5D": "3 或 0 个关键张。",
            "5H": "2 个关键张，无将牌 Q。",
            "5S": "2 个关键张，有将牌 Q。",
        }.get(bid)

    overcall = interfered
    next_bid = _next_bid_after(overcall)
    next_next_bid = _next_bid_after(next_bid)
    return {
        "X": "1 或 4 个关键张。",
        "Pass": "3 或 0 个关键张。",
        next_bid: "2 个关键张，无将牌 Q。",
        next_next_bid: "2 个关键张，有将牌 Q。",
    }.get(bid)


def keycard_explanations(auction):
    """Return Roman Key Card Blackwood explanations for a 4NT sequence."""
    if not isinstance(auction, list):
        return {}

    ask_index = next(
        (index for index in range(len(auction) - 1, -1, -1) if auction[index] == "4NT"),
        None,
    )
    if ask_index is None:
        return {}

    calls_before_ask = [
        bid
        for bid in auction[:ask_index + 1]
        if bid not in ("Pass", "P")
    ]
    if calls_before_ask[-3:] in (["1NT", "4C", "4NT"], ["2NT", "4C", "4NT"]):
        return {}

    trump = _keycard_trump(auction, ask_index)
    explanations = {
        "4NT": (
            f"罗马关键张问叫，当前将牌为 {SUIT_NAMES[trump]}。"
            if trump
            else "罗马关键张问叫，当前未能确定将牌。"
        ),
    }

    first_follow_up = next(
        (
            index
            for index in range(ask_index + 1, len(auction))
            if auction[index] not in ("Pass", "P")
        ),
        None,
    )
    interfered = None
    response_index = None
    if first_follow_up is not None:
        if (
            _bid_level(auction[first_follow_up]) == 5
            and _bid_suit(auction[first_follow_up])
            and first_follow_up % 2 != ask_index % 2
        ):
            interfered = auction[first_follow_up]
            response_index = first_follow_up + 1
        elif first_follow_up % 2 == ask_index % 2:
            response_index = first_follow_up

    if interfered:
        for bid in ("X", "Pass", _next_bid_after(interfered), _next_bid_after(_next_bid_after(interfered))):
            meaning = _keycard_response_meaning(bid, trump, interfered)
            if meaning:
                explanations[bid] = meaning
    else:
        for bid in ("5C", "5D", "5H", "5S"):
            meaning = _keycard_response_meaning(bid, trump, False)
            if meaning:
                explanations[bid] = meaning

    if response_index is not None and response_index < len(auction):
        response = auction[response_index]
        asker_index = response_index + 2
        if asker_index < len(auction):
            q_bid = auction[asker_index]
            response_is_14_or_30 = response in ("5C", "5D", "X")
            if q_bid == "5NT":
                explanations["5NT"] = "关键张以及将牌 Q 齐全，询问旁花 K。"
                for level in (5, 6, 7):
                    for suit in ("C", "D", "H", "S"):
                        explanations[f"{level}{suit}"] = "自然叫。"
                if trump:
                    explanations[f"6{trump}"] = "无低于将牌花色级别的 K，可能有高于将牌花色级别的 K。"
                    explanations[f"7{trump}"] = "有额外的长套赢墩来源，不需要其他 K。"
            elif (
                response_is_14_or_30
                and _bid_level(q_bid) == 5
                and _bid_suit(q_bid)
                and _bid_suit(q_bid) != trump
            ):
                explanations[q_bid] = "最经济的非将牌花色问将牌 Q。"
                if trump and ("C", "D", "H", "S").index(_bid_suit(q_bid)) > ("C", "D", "H", "S").index(trump):
                    explanations[f"6{trump}"] = "无将牌 Q。"
                    explanations["5NT"] = "有将牌 Q，但没有边花 K，或有边花 K 但不能越过 6 阶将牌。"
                    explanations[f"7{trump}"] = "有将牌 Q，且有额外赢墩或可修长套赢墩，或限制性叫牌中有额外的 K。"
                    for suit in ("C", "D", "H", "S"):
                        if suit == trump:
                            continue
                        bid = f"5{suit}"
                        if ("C", "D", "H", "S").index(suit) < ("C", "D", "H", "S").index(trump):
                            explanations[bid] = "有将牌 Q 及该花色 K。"
                        else:
                            explanations[bid] = "有将牌 Q 及该花色 K，并有额外实力，保证能打 6NT。"
                else:
                    explanations[f"5{trump}"] = "无将牌 Q。"
                    explanations[f"6{trump}"] = "有将牌 Q，但没有边花 K。"
                    for suit in ("C", "D", "H", "S"):
                        if suit != trump:
                            explanations[f"5{suit}"] = "有将牌 Q 及该花色 K，按最低花色 K 顺序答叫。"

    if response_index is not None and response_index + 2 < len(auction):
        if auction[response_index + 2] == "5NT":
            explanations["5NT"] = "关键张以及将牌 Q 齐全，询问旁花 K。"
            for level in (5, 6, 7):
                for suit in ("C", "D", "H", "S"):
                    explanations.setdefault(f"{level}{suit}", "自然叫。")
            if trump:
                explanations[f"6{trump}"] = "无低于将牌花色级别的 K，可能有高于将牌花色级别的 K。"
                explanations[f"7{trump}"] = "有额外的长套赢墩来源，不需要其他 K。"

    return explanations


def is_opening_auction(auction):
    """Return whether the first non-Pass bid follows only Passes."""
    if not isinstance(auction, list):
        return False

    for bid in auction:
        if bid not in ("Pass", "P"):
            return True
    return True


def response_opening(auction):
    """Return the opening bid for an uncontested response sequence."""
    if not isinstance(auction, list):
        return None

    first_bid_index = next(
        (index for index, bid in enumerate(auction) if bid not in ("Pass", "P")),
        None,
    )
    if first_bid_index is None:
        return None

    opening_bid = auction[first_bid_index]
    if (
        opening_bid not in RESPONSE_EXPLANATIONS
        or first_bid_index + 1 >= len(auction)
        or auction[first_bid_index + 1] not in ("Pass", "P")
    ):
        return None

    return opening_bid


def build_bid_explanations(auction=None, dealer="N", seat="S"):
    opening_auction = is_opening_auction(auction)
    response_bid = response_opening(auction)
    convention_bids = convention_explanations(auction, dealer, seat)
    keycard_bids = keycard_explanations(auction)
    explanations = [
        {
            "bid": "Pass",
            "meaning": keycard_bids.get(
                "Pass",
                convention_bids.get("Pass", "一般 11 点以下。"),
            ),
        },
        {
            "bid": "X",
            "meaning": keycard_bids.get(
                "X",
                convention_bids.get(
                    "X",
                    "加倍，通常表示对对手叫品有竞争性意见，具体含义取决于叫牌进程。",
                ),
            ),
        },
        {
            "bid": "XX",
            "meaning": "再加倍，通常表示对加倍有较强牌力或希望继续竞争。",
        },
    ]

    for level in range(1, 8):
        for suit in ("C", "D", "H", "S", "NT"):
            bid = f"{level}{suit}"
            if bid in keycard_bids:
                meaning = keycard_bids[bid]
            elif bid in convention_bids:
                meaning = convention_bids[bid]
            elif response_bid and bid in RESPONSE_EXPLANATIONS[response_bid]:
                meaning = RESPONSE_EXPLANATIONS[response_bid][bid]
            elif opening_auction and bid in OPENING_EXPLANATIONS:
                meaning = OPENING_EXPLANATIONS[bid]
            elif bid == "1NT":
                meaning = "15-17 点均型，可能有 5 张高花或 6 张低花。"
            else:
                meaning = (
                    f"{level}{SUIT_NAMES[suit]}，表示愿意在 {SUIT_NAMES[suit]} "
                    "作为将牌的情况下承担相应墩数，具体含义取决于叫牌进程。"
                )
            explanations.append({"bid": bid, "meaning": meaning})

    return explanations


def bid_rank(bid):
    levels = {"C": 1, "D": 2, "H": 3, "S": 4, "NT": 5}
    return int(bid[0]) * 5 + levels[bid[1:]]


def validate_auction(auction, dealer="N"):
    """Validate bidding order and report whether three passes ended the auction."""
    if not isinstance(auction, list):
        return False, False, "auction 必须是数组。"

    seats = ["W", "N", "E", "S"]
    if dealer not in seats:
        return False, False, "dealer 必须是 W、N、E 或 S。"

    last_contract = None
    last_non_pass = None
    consecutive_passes = 0

    for index, bid in enumerate(auction):
        seat = seats[(seats.index(dealer) + index) % len(seats)]
        if bid in ("Pass", "P"):
            consecutive_passes += 1
            max_passes = 3 if last_contract else 4
            if consecutive_passes > max_passes:
                return False, False, "Pass 次数超过当前叫牌阶段的规则限制。"
            continue

        consecutive_passes = 0
        if bid in ("X", "XX"):
            if bid == "X":
                if (
                    last_non_pass is None
                    or last_non_pass[0] in ("X", "XX")
                    or last_contract is None
                    or last_contract[1] in (seat, seats[(seats.index(seat) + 2) % 4])
                ):
                    return False, False, "当前叫牌不能加倍。"
            elif (
                last_non_pass is None
                or last_non_pass[0] != "X"
                or last_non_pass[1] in (seat, seats[(seats.index(seat) + 2) % 4])
            ):
                return False, False, "当前叫牌不能再加倍。"
            last_non_pass = (bid, seat)
            continue

        if len(bid) < 2 or bid[0] not in "1234567" or bid[1:] not in SUIT_NAMES:
            return False, False, f"无效叫品：{bid}。"
        if last_contract and bid_rank(bid) <= bid_rank(last_contract[0]):
            return False, False, "新叫品必须高于当前定约。"

        last_contract = (bid, seat)
        last_non_pass = (bid, seat)

    auction_ended = (
        last_contract is None and consecutive_passes == 4
    ) or (
        last_contract is not None and consecutive_passes == 3
    )
    return True, auction_ended, ""


BID_EXPLANATIONS = build_bid_explanations()


class BiddingApiHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path != "/explain-bids":
            self._send_json(404, {"error": "Not found"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            request_body = self.rfile.read(content_length)
            request = json.loads(request_body or b"{}")
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "Request body must be valid JSON"})
            return

        auction = request.get("auction") if isinstance(request, dict) else None
        dealer = request.get("dealer", "N") if isinstance(request, dict) else "N"
        candidate_bid = request.get("candidate_bid") if isinstance(request, dict) else None
        effective_auction = list(auction) if isinstance(auction, list) else auction
        if candidate_bid is not None:
            if not isinstance(effective_auction, list):
                effective_auction = []
            effective_auction.append(candidate_bid)

        valid, auction_ended, error = validate_auction(effective_auction, dealer)
        response_seat = request.get("seat", "S") if isinstance(request, dict) else "S"
        if candidate_bid is not None and dealer in ("N", "E", "S", "W"):
            seats = ["W", "N", "E", "S"]
            response_seat = seats[
                (seats.index(dealer) + len(effective_auction) - 1) % 4
            ]
        self._send_json(200, {
            "bids": build_bid_explanations(
                effective_auction,
                dealer,
                response_seat,
            ),
            "valid": valid,
            "auction_ended": auction_ended,
            "error": error,
        })

    def log_message(self, format_string, *args):
        print(f"[bidding-api] {self.address_string()} - {format_string % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), BiddingApiHandler)
    print(f"Bidding explanation API listening on http://{HOST}:{PORT}/explain-bids")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping bidding explanation API.")
        server.server_close()
