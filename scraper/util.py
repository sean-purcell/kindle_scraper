def html_encode_unicode(text):
    return "".join(c if ord(c) < 128 else "&#{};".format(ord(c)) for c in text)

def format_chapter(title, text, author):
    TEMPLATE = """
    <DOCTYPE html>
    <html lang="en">
    <head>
        <title>{title}</title>
        <meta name="author" content="{author}"></meta>
    </head>
    <body>
        <h3>{title}</h3>
        <div align="left">
        {text}
        </div>
    </body>
    </html>
    """

    escaped = html_encode_unicode(text)
    return TEMPLATE.format(author=author, title=title, text=escaped)

def format_ebook(title, author, chapters):
    CHAPTER_TEMPLATE = """
    <h1 class="chapter">{title}</h1>
    <div align="left">
        {content}
    </div>
    """

    TEMPLATE = """
    <DOCTYPE html>
    <html lang="en">
    <head>
        <title>{title}</title>
        <meta name="author" content="{author}"></meta>
    </head>
    <body>
        {chapters}
    </body>
    </html>
    """

    formatted_chapters = [CHAPTER_TEMPLATE.format(
        title=ctitle, content=content) for ctitle, content in chapters]
    return TEMPLATE.format(
            author=author,
            title=title,
            chapters='\n'.join(formatted_chapters))
