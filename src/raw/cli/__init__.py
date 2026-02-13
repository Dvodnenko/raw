import sys

from ..domain import DomainError
from ..infrastructure import InfrastructureError
from .parsers import build_parser


def main(argv=None):
    parser = build_parser()

    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        parser.print_help()
        return 0

    args = parser.parse_args(argv)

    try:
        args.handler(args)
    except (DomainError, InfrastructureError) as e:
        print(e.message, file=sys.stderr)
        sys.exit(1)
    except (KeyboardInterrupt):
        print("cancelled by user")
        exit(0)
    except Exception as e:
        print("unexpected error")
        if args.D:
            raise e
        sys.exit(1)


if __name__ == "__main__":
    main()
