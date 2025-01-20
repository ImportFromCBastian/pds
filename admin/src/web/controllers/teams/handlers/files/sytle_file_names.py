def style(url: str) -> str:
    """
    Styles the file name.
    """
    return url.split("/")[-1].split("?")[0].replace("_", " ").capitalize().split(".")[0]
