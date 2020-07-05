import configargparse

_flags = None

def get_flags():
    global _flags

    if _flags:
        return _flags

    p = configargparse.ArgParser(default_config_files=["CONFIG"])

    # Config options
    p.add("--email_token", required=True)
    p.add("--gmail_discovery", required=True)
    p.add("--src_address", required=True)
    p.add("--dst_address", required=True)
    p.add("--state_file", required=True)
    p.add("--modules", required=True)

    p.add("--no-send", help="update state without sending", default=False)
    p.add("--write-to-file", help="write documents to files", default=False)

    _flags = p.parse_args()
    return _flags
