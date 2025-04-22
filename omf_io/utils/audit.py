import json
import os
from dataclasses import field, asdict, dataclass
from datetime import datetime
from typing import Literal


def get_username():
    try:
        return os.getlogin()
    except OSError:
        return os.environ.get('USER') or os.environ.get('USERNAME') or 'unknown_user'

@dataclass
class ChangeMessage:
    """Dataclass to mange auditability"""
    element: str
    action: Literal['create', 'update', 'delete']
    description: str
    user: str = field(default_factory=get_username)
    timestamp: str = field(default_factory=datetime.now)

    def __str__(self):
        return json.dumps(asdict(self), default=str)