from datetime import timezone

from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator


class UTCDateTime(TypeDecorator):
    """Armazena datas em UTC e recupera datetimes com fuso UTC."""

    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Converte para UTC antes de armazenar."""

        if value is None:
            return None

        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(
                "A data deve conter informação de fuso horário."
            )

        return value.astimezone(timezone.utc).replace(tzinfo=None)

    def process_result_value(self, value, dialect):
        """Reconstitui o fuso UTC após a leitura."""

        if value is None:
            return None

        return value.replace(tzinfo=timezone.utc)