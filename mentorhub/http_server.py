import http.server
import json

from mentorhub.domain import add_goal
from mentorhub.storage import JsonStorage
from mentorhub.storage_base import (
    StorageDecodeError,
    StorageNotFoundError,
    StorageSaveDataError,
)


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header(keyword="content-type", value="application/json")
            self.end_headers()
            message = json.dumps({"status": "OK"})
            message_bytes = message.encode("utf-8")
            self.wfile.write(message_bytes)
        elif self.path == "/goals":
            try:
                storage = JsonStorage("data.json")
                data = storage.load()
                goals = {}
                for goal in data.values():
                    goals[goal.title] = [
                        {"title": t.title, "done": t.done} for t in goal.tasks
                    ]
                message = json.dumps(goals, ensure_ascii=False)
                message_bytes = message.encode("utf-8")
                self.send_response(200)
                self.send_header(keyword="content-type", value="application/json")
                self.end_headers()
                self.wfile.write(message_bytes)
            except (StorageDecodeError, StorageNotFoundError):
                self.send_response(500)
                self.send_header(keyword="content-type", value="application/json")
                self.end_headers()
                message = json.dumps(
                    {"response": "Внутренняя ошибка сервера"}, ensure_ascii=False
                )
                message_bytes = message.encode("utf-8")
                self.wfile.write(message_bytes)
        else:
            self.send_response(404)
            self.send_header(keyword="content-type", value="application/json")
            self.end_headers()
            message = json.dumps({"response": "Ресурс не найден"}, ensure_ascii=False)
            message_bytes = message.encode("utf-8")
            self.wfile.write(message_bytes)

    def do_POST(self):
        if self.path == "/goals":
            try:
                length = int(self.headers.get("content-length"))
                if length <= 0:
                    raise ValueError
                message_bytes = self.rfile.read(length)
                message = message_bytes.decode("utf-8")
                data_income = json.loads(message)
                if (
                    isinstance(data_income, dict)
                    and "title" in data_income
                    and isinstance(data_income["title"], str)
                    and data_income["title"].strip()
                ):
                    storage = JsonStorage("data.json")
                    goals = storage.load()
                    created = add_goal(goals, data_income["title"])
                    if created:
                        storage.save(goals)
                        self.send_response(201)
                        self.send_header(
                            keyword="content-type", value="application/json"
                        )
                        self.end_headers()
                        message = json.dumps(
                            {"response": "Цель создана"}, ensure_ascii=False
                        )
                        message_bytes = message.encode("utf-8")
                        self.wfile.write(message_bytes)
                        print(created)
                    else:
                        self.send_response(409)
                        self.send_header(
                            keyword="content-type", value="application/json"
                        )
                        self.end_headers()
                        message = json.dumps(
                            {"response": "Цель уже создана"}, ensure_ascii=False
                        )
                        message_bytes = message.encode("utf-8")
                        self.wfile.write(message_bytes)
                else:
                    self.send_response(400)
                    self.send_header(keyword="content-type", value="application/json")
                    self.end_headers()
                    message = json.dumps(
                        {"response": "Некорректный формат данных"}, ensure_ascii=False
                    )
                    message_bytes = message.encode("utf-8")
                    self.wfile.write(message_bytes)
            except (json.JSONDecodeError, TypeError, ValueError):
                self.send_response(400)
                self.send_header(keyword="content-type", value="application/json")
                self.end_headers()
                message = json.dumps(
                    {"response": "Некорректный формат данных"}, ensure_ascii=False
                )
                message_bytes = message.encode("utf-8")
                self.wfile.write(message_bytes)
            except (StorageDecodeError, StorageNotFoundError, StorageSaveDataError):
                self.send_response(500)
                self.send_header(keyword="content-type", value="application/json")
                self.end_headers()
                message = json.dumps(
                    {"response": "Внутренняя ошибка сервера"}, ensure_ascii=False
                )
                message_bytes = message.encode("utf-8")
                self.wfile.write(message_bytes)
        else:
            self.send_response(404)
            self.send_header(keyword="content-type", value="application/json")
            self.end_headers()
            message = json.dumps({"response": "Ресурс не найден"}, ensure_ascii=False)
            message_bytes = message.encode("utf-8")
            self.wfile.write(message_bytes)


server = http.server.HTTPServer(("127.0.0.1", 8000), Handler)
server.serve_forever()
