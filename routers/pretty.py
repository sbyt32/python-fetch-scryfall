import json
from fastapi import Response


class PrettyJSONResp(Response):
    media_type = "application/json"

    def render(self, content) -> bytes:
        return json.dumps(content,ensure_ascii=False, allow_nan=False,indent=3,separators=(", ", ": ")).encode('utf-8')