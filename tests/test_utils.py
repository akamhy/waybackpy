from waybackpy import __version__
from waybackpy.utils import DEFAULT_USER_AGENT


def test_default_user_agent() -> None:
    assert (
        DEFAULT_USER_AGENT
        == f"waybackpy {__version__} - https://github.com/akamhy/waybackpy"
    )
