def list_to_in_phrase(lst: list, with_quotes: bool = True) -> str:
    """
    Converts string list into a sql "IN (...)" phrase
    Args: lst (list): items to convert
          with_quotes (bool, optional): whether to quote the items. Defaults to true
    Returns: str: "IN (...)" phrase
    """
    if with_quotes:
        quoted = [f"'{p}'" for p in lst]
    else:
        quoted = [f"{p}" for p in lst]
    return f" IN ({', '.join(quoted)}) "