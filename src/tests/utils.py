from wagtail import models


def get_full_page_path(page: models.Page) -> str:
    root = page.get_root()
    if root.id == page.id:
        return "/"
    pages = [page.get_url()]

    while page := page.get_parent():
        if page.id == root.id:
            break

        pages.append(page.get_url())

    return "/" + "".join(reversed(pages))
