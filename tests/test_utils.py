from urllib.parse import quote

from hw.utils import uri_to_dict


def test_url_to_dict():
    """Проверяем конвертацию различных урлов в словарь."""
    assert uri_to_dict("http://host") == {
        "HOST": "host",
        "USER": "",
        "PASSWORD": "",
        "PORT": "",
        "DBNAME": "",
    }
    assert uri_to_dict("http://host:port") == {
        "HOST": "host",
        "USER": "",
        "PASSWORD": "",
        "PORT": "port",
        "DBNAME": "",
    }
    assert uri_to_dict("http://@host:port") == {
        "HOST": "host",
        "USER": "",
        "PASSWORD": "",
        "PORT": "port",
        "DBNAME": "",
    }
    assert uri_to_dict("http://:@host:port") == {
        "HOST": "host",
        "USER": "",
        "PASSWORD": "",
        "PORT": "port",
        "DBNAME": "",
    }
    assert uri_to_dict("http://login:@host:port") == {
        "HOST": "host",
        "USER": "login",
        "PASSWORD": "",
        "PORT": "port",
        "DBNAME": "",
    }
    assert uri_to_dict("http://login:password@host:port") == {
        "HOST": "host",
        "USER": "login",
        "PASSWORD": "password",
        "PORT": "port",
        "DBNAME": "",
    }
    assert uri_to_dict("http://login:password@host:port/path") == {
        "HOST": "host",
        "USER": "login",
        "PASSWORD": "password",
        "PORT": "port",
        "DBNAME": "path",
    }
    assert uri_to_dict("http://log in:password@host:port") == {
        "HOST": "host",
        "USER": "log in",
        "PASSWORD": "password",
        "PORT": "port",
        "DBNAME": "",
    }
    # https://django-environ.readthedocs.io/en/latest/tips.html#using-unsafe-characters-in-urls
    quoted_pass = quote("pass?word")
    assert uri_to_dict(f"http://login:{quoted_pass}@host:port") == {
        "HOST": "host",
        "USER": "login",
        "PASSWORD": "pass?word",
        "PORT": "port",
        "DBNAME": "",
    }
