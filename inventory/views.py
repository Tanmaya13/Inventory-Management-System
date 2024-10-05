from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotAuthenticated

from inventory.models import Inventory
from inventory.validators.validatory import PayloadValidator
from inventory.serializers import InventorySerializer

import logging
logger = logging.getLogger(__name__)

CACHE_KEY_PREFIX = "inventory_item"

class ItemCreateViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    def post(self, request):
        '''this POST method will check JWT authentication
           validate the payload
           create object if item does not exists with 201 status code
           return item details if already exists in DB with 400 status code
           set up cache
           return the response as serialized data
        '''
        logger.info("Entering into ItemCreateViewSet post method")

        user = request.user
        if not user.is_authenticated:
            raise NotAuthenticated()

        payload = request.data
        name = payload.get("name")
        description = payload.get("description")
        stock_count = payload.get("stock_count")

        # PAYLOAD VALIDATION
        validate_keys = ["name", "description", "stock_count"]
        validate = PayloadValidator(name=name, description=description, stock_count=stock_count, validate_keys=validate_keys)
        validated_payload = validate.validate()
        for key in validate_keys:
            if validated_payload[key]:
                logger.error("Invalid payload provided.")
                return Response(
                    {"INVALID_PAYLOAD": validated_payload[key]}, status=status.HTTP_400_BAD_REQUEST
                )

        try:
            inventory = Inventory.objects.get(name=name)
            serialized_data = None

            value = cache.get(f'{CACHE_KEY_PREFIX}_{str(inventory.id)}')
            if value:
                logger.info(f'Fetching item details from cache for item id :: {str(inventory.id)}')
                serialized_data = value
            else:
                cache.set(f'{CACHE_KEY_PREFIX}_{str(inventory.id)}', serialized_data)       # setting up cache
                serialized_data = InventorySerializer(inventory).data                       # data serialization
            
            return Response(
                {"item_already_exists": serialized_data}, status=status.HTTP_400_BAD_REQUEST
            )

        except Inventory.DoesNotExist:
            inventory = Inventory(name=name,
                                  description=description,
                                  stock_count=stock_count)
            inventory.save()

        return Response(
            {"SUCCESS": "Item added successfully to the inventory."}, status=status.HTTP_201_CREATED
        )
        

class ItemDetailsViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, item_id):
        '''
            this GET method will check JWT authentication
            validate the request
            try to fetch data from cache (if present)
            fetch object and serialize it to return the response
        '''
        logger.info("Entering into ItemDetailsViewSet get method")
        user = request.user
        if not user.is_authenticated:
            raise NotAuthenticated()

        # VALIDATION
        validate_keys = ["item_id"]
        validate = PayloadValidator(item_id=item_id, validate_keys=validate_keys)
        validated_payload = validate.validate()
        for key in validate_keys:
            if validated_payload[key]:
                return Response(
                    {"INVALID_REQUEST": validated_payload[key]}, status=status.HTTP_404_NOT_FOUND
                )
        
        # CACHE 
        cache_value = cache.get(f"{CACHE_KEY_PREFIX}_{str(item_id)}")
        if cache_value:
            logger.debug(f"Fetching item details from cache for item id :: {str(item_id)}")
            return Response(
                {"inventory_item_details": cache_value}, status=status.HTTP_200_OK
        )
        
        # OBJECT RETRIEVAL AND SERIALIZATION
        inventory_obj = Inventory.objects.get(id=item_id)
        serialized_data = InventorySerializer(inventory_obj).data

        logger.debug(f"Setting up cache for item id :: {str(item_id)}")
        cache.set(f"{CACHE_KEY_PREFIX}_{str(item_id)}", serialized_data)

        return Response(
            {"inventory_item_details": serialized_data}, status=status.HTTP_200_OK
        )
        
    def put(self, request, item_id):
        '''
            this PUT method will check JWT authentication
            validate the payload
            update the item details
            clear the cache
            return serialized response of the updated item
        '''
        logger.info("Entering into ItemDetailsViewSet put method")

        user = request.user
        if not user.is_authenticated:
            raise NotAuthenticated()

        payload = request.data
        name = payload.get("name")
        description = payload.get("description")
        stock_count = payload.get("stock_count")

        # VALIDATION
        validate_keys = ["name", "description", "stock_count", "item_id"]
        validate = PayloadValidator(name=name, description=description, stock_count=stock_count, item_id=item_id, validate_keys=validate_keys)
        validated_payload = validate.validate()
        for key in validate_keys:
            if validated_payload[key]:
                return Response(
                    {"INVALID_REQUEST": validated_payload[key]}, status=status.HTTP_404_NOT_FOUND
                )
        
        # OBJECT RETRIEVAL
        inventory_obj = Inventory.objects.get(id=item_id)
        inventory_obj.name = name
        inventory_obj.description = description
        inventory_obj.stock_count = stock_count

        # CACHE CLEAR
        cache.delete(f'{CACHE_KEY_PREFIX}_{str(item_id)}')

        # SAVING UPDATED INFO
        inventory_obj.save()

        # DATA SERIALIZATION
        serialized_data = InventorySerializer(inventory_obj).data

        return Response(
            {"updated_item_details": serialized_data}, status=status.HTTP_200_OK
        )

    def delete(self, request, item_id):
        '''
            this DELETE method will check JWT authentication
            validate the item id
            delete the item from the inventory DB
            clear cache
        '''
        logger.info("Entering into ItemDetailsViewSet delete method")

        user = request.user
        if not user.is_authenticated:
            raise NotAuthenticated()

        # VALIDATION
        validate_keys = ["item_id"]
        validate = PayloadValidator(item_id=item_id, validate_keys=validate_keys)
        validated_payload = validate.validate()
        for key in validate_keys:
            if validated_payload[key]:
                logger.error(f"error while deleting item :: {str(item_id)}")
                return Response(
                    {"INVALID_REQUEST": validated_payload[key]}, status=status.HTTP_404_NOT_FOUND
                )
        
        # OBJECT RETRIEVAL
        inventory_obj = Inventory.objects.get(id=item_id)

        # CACHE CLEAR
        cache.delete(f'{CACHE_KEY_PREFIX}_{str(item_id)}')

        # DELETE RECORD
        inventory_obj.delete()

        return Response(
            {"SUCCESS": "Deleted your item from the inventory successfully."}, status=status.HTTP_200_OK
        )
