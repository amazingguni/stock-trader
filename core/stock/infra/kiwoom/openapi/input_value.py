from dataclasses import dataclass


@dataclass
class InputValue:
    s_id: str
    s_value: 'typing.Any'
