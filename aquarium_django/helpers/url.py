from typing import Dict, Any

STATUS_CODES = {
    1: "OK",
    -1: "ERR"
}


def generate_json_response(code: int, msg: str, contents: Dict[str, Any]) -> Dict[Any, Any]:
    """
    Method generates base json response
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
