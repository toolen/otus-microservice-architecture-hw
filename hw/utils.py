from typing import Optional, TypedDict, Union
from urllib.parse import ParseResult, unquote, urlparse


class UriAsDict(TypedDict):
    """Класс для типизации ответа функции url_e."""

    HOST: str
    USER: Optional[str]
    PASSWORD: Optional[str]
    PORT: Optional[str]
    DBNAME: str


def uri_to_dict(value: str, convert_port_to_int: bool = False) -> Optional[UriAsDict]:
    """
    Преобразует строку вида protocol://login:password@host:port/dbname
    в словарь.
    """
    login = ""
    password = ""  # noqa: S105
    parse_result: ParseResult = urlparse(value)
    scheme = parse_result.scheme
    netloc = parse_result.netloc
    path = parse_result.path
    port = ""
    if scheme and netloc:
        if "@" in netloc:
            netloc_splitted = netloc.split("@")

            if len(netloc_splitted) == 2:
                creds, host = netloc_splitted
            else:
                host = netloc_splitted.pop()
                creds = "@".join(netloc_splitted)

            if creds and ":" in creds:
                login, password = creds.split(":")
        else:
            host = netloc

        if path:
            path = path[1:]

        if ":" in host:
            host, port = host.split(":")

        return {
            "HOST": host,
            "USER": login,
            "PASSWORD": unquote(password),
            "PORT": port,
            "DBNAME": path,
        }
    return None
