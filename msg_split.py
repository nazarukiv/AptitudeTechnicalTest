from bs4 import BeautifulSoup, Tag
from typing import Generator

MAX_LEN = 4096

def split_message(source: str, max_len=MAX_LEN) -> Generator[str, None, None]:
    soup = BeautifulSoup(source, 'html.parser')

    def extract_text_and_tags(tag: Tag, length: int) -> str:
        html = ''
        for child in tag.children:
            if isinstance(child, Tag):
                child_html = str(child)
                if len(child_html) + len(html) <= length:
                    html += child_html
                else:
                    return html
            else:
                remaining_len = length - len(html)
                html += child[:remaining_len]
                break
        return html

    remaining_html = str(soup)
    while remaining_html:
        if len(remaining_html) <= max_len:
            yield remaining_html
            break

        fragment = extract_text_and_tags(soup, max_len)
        if not fragment:
            raise ValueError(f"Cannot split message to fit within {max_len} characters.")
        yield fragment

        remaining_html = remaining_html[len(fragment):]
        soup = BeautifulSoup(remaining_html, 'html.parser')


