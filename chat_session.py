from typing import TypeVar, Generic
from dataclasses import dataclass, asdict
import requests
import json
from logger import log
from exec_time import execution_time


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

# @dataclass
# class ChatResponse:
    # model: str
    # created_at: str
    # message: Message
    # done: bool
    # total_duration: int
    # load_duration: int
    # prompt_eval_duration: int
    # eval_count: int
    # eval_duration: int
    # prompt_eval_count: int = None

    # # def __init__(self, **kwargs) -> None:
    # #     for key, value in self.__dict__.items():
    # #         log(key, value)
    # #         if key in kwargs:
    # #             self[key] = kwargs[key]


    # @classmethod
    # def from_dict(cls, data):
    #     data['message'] = Message.from_dict(data['message'])
    #     return cls(**data)

    # def to_dict(self):
    #     data = asdict(self)
    #     # data['message'] = asdict(data['message'])
    #     return data


@dataclass
class ChatResponse:
    message: Message

    @classmethod
    def from_dict(cls, data):
        data['message'] = Message.from_dict(data['message'])
        return cls(**data)

    def to_dict(self):
        data = asdict(self)
        # data['message'] = asdict(data['message'])
        return data    

class Chat:
    _session_id: str
    _context: str
    _model_name: str
    _chat_content: list[Message] = []
    _system="""
        You are Enigma, an LLM developed by Team Strivers to summarize legal documents and extract key insights. Your primary function is to respond to questions related to specific paragraphs within these documents.

        Master Prompt:

        Input: [Contextual Paragraph]

        you will be given the input and you have to provide the answer of the question based on the given input.

        Don't provide the answer of the question if it is not related to the context paragraph.
    """

    def __init__(self, id: str, model_name: str = "llama2"):
        self._session_id = id
        self._model_name = model_name

    def set_context(self, context: str):
        self._context = context
        self._chat_content.append(
            Message(f"[Context] \n{self._context} [Context] \n[Provide Answer to the question based on this context.]"))
        # return self._get_model_response()
        return "done"

    def get_context(self):
        return self._context

    def _get_model_response(self) -> ChatResponse:
        response = requests.post(
            f"https://api.cloudflare.com/client/v4/accounts/1c7120b407404a4d257e57af5a88f88f/ai/run/@cf/meta/llama-2-7b-chat-fp16",
            headers={"Authorization": f"Bearer 3ti0Lh8dnLmIpbGi-0n7Z9o58JAoBgkBQh3k9tPh"},
            json={
                "messages": [
                {"role": "system", "content": self._system},
                    *self._chat_content
                ]
            }
        )

        result = response.json()
        if result["success"]:
            log(result["result"]["response"])
            self._chat_content.append(Message(role="assistant", content=result["result"]["response"]))
        return result

    def send_message(self, inp: str, bot=False):
        if bot:
            self._chat_content.append(Message(role="assistant", content=inp))
        self._chat_content.append(Message(inp))
        return self._get_model_response()
    
    def get_messages(self):
        return [message.__dict__ for message in self._chat_content]

    def get_session_details(self):
        return {
            "session_id": self._session_id,
            "context": self._context,
            "model_name": self._model_name,
            "messages": self.get_messages()[1:]
        }

    def get_session_id(self):
        return self._session_id



class ChatSession:
    _chat_sessions: list[Chat] = []

    @execution_time
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
        else:
            self._chat_sessions.append(Chat(id))
        return self._chat_sessions[-1]




if __name__=="__main__":
    message = Message("Hi")
    print(json.dumps(message))

