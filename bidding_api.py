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
    "2C": "22 点以上任意牌型，或 18 点以上且有 9 张以上赢墩。",
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
}


def is_opening_auction(auction):
    """Return whether the first non-Pass bid follows only Passes."""
    if not isinstance(auction, list):
        return False

    for bid in auction:
        if bid not in ("Pass", "P"):
            return True
    return True


def response_opening(auction):
    """Return the opening bid for an uncontested 1m response sequence."""
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


def build_bid_explanations(auction=None):
    opening_auction = is_opening_auction(auction)
    response_bid = response_opening(auction)
    explanations = [
        {
            "bid": "Pass",
            "meaning": "一般 11 点以下。",
        },
        {
            "bid": "X",
            "meaning": "加倍，通常表示对对手叫品有竞争性意见，具体含义取决于叫牌进程。",
        },
        {
            "bid": "XX",
            "meaning": "再加倍，通常表示对加倍有较强牌力或希望继续竞争。",
        },
    ]

    for level in range(1, 8):
        for suit in ("C", "D", "H", "S", "NT"):
            bid = f"{level}{suit}"
            if response_bid and bid in RESPONSE_EXPLANATIONS[response_bid]:
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
        self._send_json(200, {"bids": build_bid_explanations(auction)})

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
