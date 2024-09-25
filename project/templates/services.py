# pylint: disable=import-outside-toplevel
from templates.api.serializers import PaperDocumentSerializer


def attach_document(request):
    serializer = PaperDocumentSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data


def clean_mob_number(phone):
    try:  # checking non-numerics
        int(phone)
    except ValueError:
        return None
    has_country_code = phone.startswith("+977")
    if has_country_code and len(phone) == 14:
        return f"+{int(phone)}"
    if len(phone) == 10:
        return f"+977{int(phone)}"
    return None


def archive_multiple_papers(paper_ids: list[int]):
    ...


def read_multiple_papers(paper_ids: list[int]):
    ...


def unread_multiple_papers(paper_ids: list[int]):
    ...


def pin_multiple_papers(paper_ids: list[int]):
    ...


def unpin_multiple_papers(paper_ids: list[int]):
    ...


def pin_multiple_sent_mails(paper_ids: list[int]):
    ...


def unpin_multiple_sent_mails(paper_ids: list[int]):
    ...


def find_parents_and_update(instance, data: dict):
    ...
