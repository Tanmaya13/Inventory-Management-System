from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from inventory.models import Inventory
from inventory.serializers import InventorySerializer
from inventory.views import ItemCreateViewSet 


from unittest.mock import patch


class TestItemCreateViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            "name": "Test Item",
            "description": "This is a test item",
            "stock_count": 10
        }

    def test_create_item_success(self):
        response = self.client.post('/inventory-manager/items/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"SUCCESS": "Item added successfully to the inventory."})

        item = Inventory.objects.get(name=self.valid_payload["name"])
        self.assertEqual(item.description, self.valid_payload["description"])
        self.assertEqual(item.stock_count, self.valid_payload["stock_count"])

    def test_create_item_duplicate(self):
        # Creating an item beforehand
        Inventory.objects.create(name="Test Item", description="This is a test item", stock_count=10)

        response = self.client.post('/inventory-manager/items/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"item_already_exists": InventorySerializer(Inventory.objects.get(name="Test Item")).data})

        # Ensuring no new object is created
        self.assertEqual(Inventory.objects.count(), 1)

    def test_create_item_missing_key(self):
        invalid_payload = {"description": "This item is missing a name", "stock_count": 5}
        response = self.client.post('/inventory-manager/items/', invalid_payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("INVALID_PAYLOAD", response.data)

    def test_create_item_invalid_value_type(self):
        invalid_payload = {"name": "Test Item", "description": "This is a test item", "stock_count": "not a number"}
        response = self.client.post('/inventory-manager/items/', invalid_payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("INVALID_PAYLOAD", response.data)



class TestItemDetailsViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_item_id = 1
        self.invalid_item_id = 9999

        # Creating an item for testing object retrieval
        Inventory.objects.create(id=self.valid_item_id, name="Test Item", description="This is a test item")

    def test_get_item_details_success_from_cache(self):
        # Simulating cache hit
        with patch('inventory.views.cache.get') as mock_cache_get:
            mock_cache_get.return_value = {"inventory_item_details": "cached_data"}

            response = self.client.get(f'/inventory-manager/items/{self.valid_item_id}/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["inventory_item_details"], {"inventory_item_details": "cached_data"})

    def test_get_item_details_success_from_db(self):
        response = self.client.get(f'/inventory-manager/items/{self.valid_item_id}/')
        self.assertEqual(response.status_code, 200)

        serialized_data = InventorySerializer(Inventory.objects.get(pk=self.valid_item_id)).data
        self.assertEqual(response.json(), {"inventory_item_details": serialized_data})

    def test_get_item_details_not_found(self):
        response = self.client.get(f'/inventory-manager/items/{self.invalid_item_id}/')
        self.assertEqual(response.status_code, 404)
        self.assertIn("INVALID_REQUEST", response.json())



class TestItemDetailsViewSetPut(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_item_id = 1 
        self.invalid_item_id = 9999
        self.valid_data = {
            "name": "Updated Item Name",
            "description": "This is an updated description",
            "stock_count": 20
        }

        # Creating an item for testing update
        self.inventory_obj = Inventory.objects.create(id=self.valid_item_id, name="Test Item", description="Initial description", stock_count=10)

    def test_update_item_success(self):
        response = self.client.put(f'/inventory-manager/items/{self.valid_item_id}/', self.valid_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("updated_item_details", response.json())

        # Verify updated data in the database
        updated_item = Inventory.objects.get(id=self.valid_item_id)
        self.assertEqual(updated_item.name, self.valid_data["name"])
        self.assertEqual(updated_item.description, self.valid_data["description"])
        self.assertEqual(updated_item.stock_count, self.valid_data["stock_count"])

    def test_update_item_not_found(self):
        response = self.client.put(f'/inventory-manager/items/{self.invalid_item_id}/', self.valid_data, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertIn("INVALID_REQUEST", response.json())

    def test_update_item_missing_data(self):
        invalid_data = {"description": "Missing name and stock count"}
        response = self.client.put(f'/inventory-manager/items/{self.valid_item_id}/', invalid_data, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertIn("INVALID_REQUEST", response.json())



class TestItemDetailsViewSetDelete(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_item_id = 1
        self.invalid_item_id = 9999

        # Creating an item for testing deletion
        self.inventory_obj = Inventory.objects.create(id=self.valid_item_id, name="Test Item", description="This is a test item")

    def test_delete_item_success(self):
        response = self.client.delete(f'/inventory-manager/items/{self.valid_item_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"SUCCESS": "Deleted your item from the inventory successfully."})

        # Verifing item is deleted from the database
        self.assertFalse(Inventory.objects.filter(id=self.valid_item_id).exists())

    def test_delete_item_not_found(self):
        response = self.client.delete(f'/inventory-manager/items/{self.invalid_item_id}/')
        self.assertEqual(response.status_code, 404)
        self.assertIn("INVALID_REQUEST", response.json())
