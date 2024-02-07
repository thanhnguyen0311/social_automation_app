from enum import Enum


class EmailEnum(Enum):
    GMAIL = "gmail.com"
    HOTMAIL = "hotmail.com"


class EmailTaskEnum(Enum):
    NO_ACTION = "Choose an action"
    CREATE = "Create email"
