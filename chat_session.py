from typing import TypeVar, Generic
from dataclasses import dataclass
import requests
import json
from logger import log


@dataclass
class Message:
    role: str
    content: str
    def __init__(self, content: str, role="user") -> None:
        self.role = role
        self.content = content

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class ChatResponse:
    model: str
    created_at: str
    message: Message
    done: bool
    total_duration: int
    load_duration: int
    prompt_eval_duration: int
    eval_count: int
    eval_duration: int

    @classmethod
    def from_dict(cls, data):
        data['message'] = Message.from_dict(data['message'])
        return cls(**data)


class Chat:
    _session_id: str
    _chat_content: list[Message] = []
    _model_name: str

    def __init__(self, id: str, model_name: str = "llama2"):
        self._session_id = id
        self._model_name = model_name

    def _get_model_response(self) -> ChatResponse:
        url = "http://localhost:11434/api/chat"
        data = {
            "model": self._model_name,
            "messages": self.get_messages(),
            "stream": False
        }
        r = requests.post(url, json=data).json()
        response = ChatResponse.from_dict(r)
        log(response)
        self._chat_content.append(Message(response.message.content, role=response.message.role))
        return response

    def send_message(self, inp: str, bot=False):
        if bot:
            self._chat_content.append(Message(role="assistant", message=inp))
        self._chat_content.append(Message(inp))
        return self._get_model_response()
    
    def get_messages(self):
        return [message.__dict__ for message in self._chat_content]


    def get_session_id(self):
        return self._session_id

class ChatSession:
    _chat_sessions: list[Chat] = []

    def get_chat_session(self, id: str, model_name: str = None):
        for session in self._chat_sessions:
            if id == session.get_session_id():
                return session
        return self.create_chat_session(id, model_name)
    
    
    def create_chat_session(self, id: str, model_name: str = None):
        for session in self._chat_sessions:
            if session.get_session_id() == id:
                return None
        if model_name:
            self._chat_sessions.append(Chat(id, model_name))
        self._chat_sessions.append(Chat(id))
        return self._chat_sessions[-1]


if __name__=="__main__":
    message = Message("Hi")
    print(json.dumps(message))

