from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict

from rest_framework.response import Response

from . import constants


class CustomBasePagination(PageNumberPagination):
    page_size = constants.DEFAULT_PAGE_SIZE
    page_size_query_param = "page_size"
    max_page_size = constants.MAX_PAGE_SIZE

    def get_paginated_response(self, data):
        previous = self.get_previous_link()
        if previous is not None:
            query = {
                k: v
                for k, v in list(
                    map(lambda x: x.split("="), previous.split("?")[1].split("&"))
                )
            }
            if "page" not in query:
                query["page"] = "1"
                query = sorted(query.items(), key=lambda x: x[0])
                previous = (
                    previous.split("?")[0]
                    + "?"
                    + "&".join([f"{i[0]}={i[1]}" for i in query])
                )

        return Response(
            OrderedDict(
                [
                    ("count", len(data)),
                    ("total_pages", self.page.paginator.num_pages),
                    ("next", self.get_next_link()),
                    ("previous", previous),
                    ("results", data),
                ]
            )
        )
