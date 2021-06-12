import argparse
from typing import Sequence
from typing import Optional

from app.create_app import create_app


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog='')
    parser.add_argument('-H', '--host', type=str, default='127.0.0.1')
    parser.add_argument('-P', '--port', type=int, default=8080)
    parser.add_argument(
            '-D', '--debug', action='store_true', default=False)
    args = parser.parse_args(argv)

    create_app().run(
        host=args.host,
        port=args.port,
        debug=args.debug,
    )

    return 0
