from inventory.models import Inventory

import logging
logger = logging.getLogger(__name__)

class PayloadValidator():
    def __init__(self, name=None, description=None, stock_count=None, item_id=None, validate_keys=None) -> None:
        self.name = name
        self.description = description
        self.stock_count = stock_count
        self.item_id = item_id
        self.payload_keys = validate_keys

    def validate_name(self):
        logger.info(f"validating name :: {self.name}")
        err_msg = None
        if self.name is None:
            err_msg = "name key is missing in the payload."
        elif not isinstance(self.name, str):
            err_msg = "Item name should be in string."
        elif len(self.name) == 0:
            err_msg = "Please provide an item name."
        return err_msg
        
    def validate_description(self):
        logger.info(f"validating description :: {self.description}")
        err_msg = None
        if self.description is None:
            err_msg = "description key is missing in the payload."
        elif not isinstance(self.description, str):
            err_msg = "Item description should be in string."
        elif len(self.description) == 0:
            err_msg = "Please provide an item description."
        return err_msg
    
    def validate_stock_count(self):
        logger.info(f"validating stock count :: {self.stock_count}")
        err_msg = None
        if self.stock_count is None:
            err_msg = "stock_count key is missing in the payload."
        elif not isinstance(self.stock_count, int):
            err_msg = "Item's stock_count should be in integers."
        elif self.stock_count < 0:
            err_msg = "Please provide valid item stock count."
        return err_msg
    
    def validate_item_id(self):
        err_msg = None
        try:
            inventory_obj = Inventory.objects.get(id=self.item_id)
        except Inventory.DoesNotExist:
            err_msg = "Item not found."
        return err_msg
    
        
    def validate(self):
        validated_payload = {}
        for key in self.payload_keys:
            validate_method = f"validate_{key}"
            method = getattr(self, validate_method)
            response = method()
            validated_payload[key] = response
        return validated_payload

        