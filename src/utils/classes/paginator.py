class Paginator:

    def __init__(self):
        pass


    def get_hits(self, ids: list, page_number: int, page_amount: int):
        "Provide the full list of ids and receive the lsit of targets in hits."

        assert isinstance(page_number, int) and page_number > 0
        assert isinstance(page_amount, int) and page_amount > 0

        minimum_amount = page_number * page_amount - page_amount
        assert minimum_amount < len(ids), "Not enough ids for pagination."

        page_start = page_number * page_amount - page_amount
        page_end = page_number * page_amount - 1

        if page_end >= len(ids): page_end = len(ids) - 1
        return ids[page_start: page_end]