from typing import Dict, Any

STATUS_CODES = {
    0: "OK",
    1: "HABITAT_DOES_NOT_EXIST",
    2: "INVALID_API_KEY",
    3: "INVALID_DATA_TOPIC",
    4: "INVALID_DATA"
}


def generate_json_response(code: int, msg: str, contents: str = "") -> Dict[Any, Any]:
    """
    Method generates base json response
    :param contents: Detailed message
    :param code: Status code to return
    :param msg: Message
    :return: Returns dict, ready to be sent or extended
    """
    return {"response": {
        "status": {
                "code": code,
                "code_str": STATUS_CODES[code]
            },
        "message": msg,
        "contents": contents
    }}
