import logging
from gforce.helpers.model_search import get_or_none, filter_or_none


class BaseRepository:
    item = None
    item_list = None
    model = None
    logger = logging.getLogger(f"Repository {model} - {__name__}")

    def __init__(
        self, *args, model=None, item=None, many=False, item_list=None, **kwargs
    ):
        self.model = model
        if not model:
            raise ReferenceError("Model Instance Not Defined")
        # Get a single Object
        if not item and not many:
            item = get_or_none(self.model, *args, **kwargs)
        self.item = item

        # Get a list or queryset of objects
        # FIXME: if we get an empty queryset here like so:
        #   # some_existing_queryset: <QuerySet: []>
        #   some_repo = SomeRepo(item_list=some_existing_queryset, many=True)
        #   it will select all model items like SELECT *
        if many and not item_list:
            item_list = filter_or_none(self.model, *args, **kwargs)
        self.item_list = item_list
        # if not item and not item_list:
        #     raise ValueError(f"No {self.model} or {self.model} List Found")

    ### TODO prefetch related and select related is not working for now, find a solution for later
    def prefetch_related(self, *args):
        """Extension of the default prefetch_related method to use on item and item_list."""
        if self.item:
            self.item = self.item.prefetch_related(*args)
        if self.item_list:
            self.item_list = self.item_list.objects.prefetch_related(*args)

    def select_related(self, *args):
        """Extension of the default select_related method to use on item and item_list."""
        if self.item:
            self.item = self.item.select_related(*args)
        if self.item_list:
            self.item_list = self.item_list.select_related(*args)

    def get_serialized_data(self, serializer_class):
        """Get the serialized Dictionary of the Instance Data based on the serializer"""
        if self.item:
            return serializer_class(self.item).data
        if self.item_list:
            return serializer_class(self.item_list, many=True).data

    def get_locked_item(self):
        """Lock the DB row for atomic Transaction"""
        self.item = self.item.select_for_update()
        return self.item

    def get_locked_item_list(self):
        """Lock the DB rows for atomic Transaction"""
        self.item_list = self.item_list.select_for_update()
        return self.item_list

    def get_fresh_item(self):
        """Get a refreshed instance of the object from Database"""
        self.item = get_or_none(self.model, id=self.item.id)
        return self.item

    def get_fresh_item_list(self):
        """Get a refreshed instances of the objects from Database"""
        id_list = [item.id for item in self.item_list]
        self.item_list = filter_or_none(self.model, id__in=id_list)
        return self.item_list
