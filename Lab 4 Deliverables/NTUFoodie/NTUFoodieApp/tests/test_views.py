from django.test import Client, TestCase, override_settings
from django.contrib.auth.models import User, Group
from NTUFoodieApp.models import *
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.messages import get_messages
from NTUFoodieApp.forms import FoodForm
from unittest.mock import patch

# Helper decorator to print success message after each test with formatting
def print_success(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        print(f"{'-'*10} {func.__name__} passed successfully {'-'*10}\n")
    return wrapper


#Test views (Black Box Testing)

class BaseTestData(TestCase):
    @classmethod
    def setUpTestData(cls):
        consumer_group, created = Group.objects.get_or_create(name="consumer")
        cls.user = User.objects.create_user(username = "testuser", password="password")
        cls.user.groups.add(consumer_group)  # Assign user to "consumer" group
        cls.consumer = Consumer.objects.create(user=cls.user)

        #cls.store = Store.objects.create(storeName = "Test Store")
        cls.canteen = Canteen.objects.create(
            location = Location.objects.create(canteenName = "Test Canteen"))
        cls.store = Store.objects.create(storeName = "Test Store", canteen = cls.canteen)
        cls.food = Food.objects.create(foodName = "Pizza", store = cls.store, rating = 0)

class CreateReviewViewsTest(BaseTestData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.create_review_url = reverse('createReview', args = [cls.consumer.id, cls.food.id])
    
    
    @print_success
    def test_createReview_get_request(self):
        self.client.login(username="testuser", password="password")
        
        url = reverse("createReview", args=[self.consumer.id, self.food.id])
        response = self.client.get(url)
        print(f"\nResponse URL: {url}")
        
        # Check that the form is displayed
        self.assertEqual(response.status_code, 200)
        print(f"Response Status Code: {response.status_code}")

        self.assertTemplateUsed(response, "NTUFoodieApp/reviewform.html")
        # Print the response URL and template used
        print("Templates used:", "NTUFoodieApp/reviewform.html")
        
        # Confirm no review was created
        self.assertEqual(Review.objects.count(), 0)
        print(f"Number of Review created: {Review.objects.count()}")


    @override_settings(APPEND_SLASH=True)
    @print_success
    def test_createReview_successful(self):

        self.client.login(username="testuser", password="password")
        form_data = {
            'rating': 4,
            'description': "Delicious food!",
        }

        response = self.client.post(self.create_review_url, data=form_data)
        print(f"\nResponse URL: {response.url}")

        # Check for redirection status code after successful review creation
        self.assertEqual(response.status_code, 302)
        print(f"Response Status Code: {response.status_code}")

         # Expected URL with trailing slash
        food_detail_url = reverse('foodDetail', args=[self.food.id])
        print(f"Food Detail URL: {food_detail_url}")
    
        self.assertRedirects(response, food_detail_url, status_code=302, target_status_code=200)
        
        
         # Check if the review was created
        self.assertEqual(Review.objects.count(), 1)
        print(f"Number of Review created: {Review.objects.count()}")

        # Check if the rating was saved correctly
        review = Review.objects.first()
        self.assertEqual(review.rating, 4.0)
        print(f"Rating saved: {review.rating}")

         # Verify if the food rating is updated
        self.food.refresh_from_db()
        self.assertEqual(self.food.rating, 4.0)
        print(f"Updated Food Rating: {self.food.rating}")

         # Check if success message was sent
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Review Created!" in str(message) for message in messages))
        print(messages)
       

class StoreownerAddListingViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        storeowner_group, created = Group.objects.get_or_create(name="storeowner")
        cls.user = User.objects.create_user(username = "teststoreowner", password="password")
        cls.user.groups.add(storeowner_group)  # Assign user to "storeowner" group
        cls.storeOwner = StoreOwner.objects.create(user=cls.user)
    
        cls.store = Store.objects.create(storeName = "Test Store")
        cls.food = Food.objects.create(store = cls.store)

        cls.url = reverse("soHome")

        cls.form_data = {
            'foodName': "Pork Chop Fried Rice",
            'price': 5.50,
            'type': "Non-Halal",
            'cuisine': "Western",
            'description': "Delicious food!",
        }

    @print_success
    def test_storeOwner_access(self):
        self.client.login(username="teststoreowner", password="password")

        response = self.client.get(self.url)
        print(f"Response URL: {self.url}")
        
        # Check that the form is displayed
        self.assertEqual(response.status_code, 200)
        print(f"Response Status Code: {response.status_code}")

        self.assertTemplateUsed(response, "NTUFoodieApp/sohome.html")
        print("Templates used:", "NTUFoodieApp/sohome.html")
        
    
    @print_success
    def test_foodListing_creation(self):
        self.client.login(username="teststoreowner", password="password")

        response = self.client.post(self.url, data=self.form_data)
        print(f"Response URL: {response.url}")

        self.assertEqual(response.status_code, 302)
        print(f"Response Status Code: {response.status_code}")

        self.assertRedirects(response, self.url) 
        print("URL Redirected")   
        
        # Check if success message was sent
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Listing Added Successfully!" in str(message) for message in messages))
        print(messages)
    
    @print_success
    def test_invalidPrice_input(self):
        self.client.login(username="teststoreowner", password="password")
        form_data_invalidPrice = self.form_data.copy()
        form_data_invalidPrice.update({

            'price': -10,
        })

        response = self.client.post(self.url, data=form_data_invalidPrice)
        print(f"Response URL: {self.url}")


        self.assertEqual(response.status_code, 200)
        print(f"Response Status Code: {response.status_code}")

        # Check if success message was sent
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Error in price: * Price cannot be negative." in str(message) for message in messages))
        print(messages)

    
class SearchFoodViewsTest(BaseTestData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.food2 = Food.objects.create(foodName = "Burger", store = cls.store, rating = 5)
        
    
    @print_success
    def test_searchFood_by_foodName(self):
        self.client.login(username="testuser", password = "password")

        response = self.client.get(reverse("searchFood"), {'searchKey': 'Pizza'})
        # Print the URL that was accessed
        print("Response URL:", response.request['PATH_INFO'])

        # Print the response content to see if "Pizza" is present and "Burger" is not
        #print("Response Content:", response.content.decode())  # Decodes bytes to a readable string
        
        #check that food page is displayed
        self.assertEqual(response.status_code, 200)
        print(f"Response Status Code: {response.status_code}")

        self.assertTemplateUsed(response, "NTUFoodieApp/foodresult.html")
        print("Templates used:", "NTUFoodieApp/foodresult.html")
        self.assertContains(response, "Pizza")
        self.assertNotContains(response, "Burger")

    
    @print_success
    def test_searchFood_by_canteenName(self):
        self.client.login(username="testuser", password = "password")

        response = self.client.get(reverse("searchFood"), {'searchKey': 'Test Canteen'})
        # Print the URL that was accessed
        print("Response URL:", response.request['PATH_INFO'])

        #print("Response Content:", response.content.decode())

        #check that food page is displayed
        self.assertEqual(response.status_code, 200)
        print(f"Response Status Code: {response.status_code}")

        self.assertTemplateUsed(response, "NTUFoodieApp/foodresult.html")
        print("Templates used:", "NTUFoodieApp/foodresult.html")
        self.assertContains(response, "Pizza")
        self.assertContains(response, "Burger")

    
    @print_success
    def test_searchFood_noResults(self):
        self.client.login(username="testuser", password = "password")

        response = self.client.get(reverse("searchFood"), {'searchKey': 'Sushi'})

        #print("Response Content:", response.content.decode())

         #check that food page is displayed
        self.assertEqual(response.status_code, 200)
        print(f"Response Status Code: {response.status_code}")

        self.assertTemplateUsed(response, "NTUFoodieApp/foodresult.html")
        print("Templates used:", "NTUFoodieApp/foodresult.html")
        self.assertNotContains(response, "Pizza")
        self.assertNotContains(response, "Burger")


class FilterFoodViewsTest(BaseTestData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.food1 = Food.objects.create(foodName = "Sushi", price = 5.50, type = "Non-Halal", cuisine = "Japanese", isDiscounted = False, discountRate = 0)
        cls.food2 = Food.objects.create(foodName = "Pasta", price = 3, type = "Halal", cuisine = "Italian", isDiscounted = False, discountRate = 0)
        cls.food3 = Food.objects.create(foodName = "Fries", price = 7, type = "Halal", cuisine = "Western", isDiscounted = True, discountRate = 10)
        cls.food1 = Food.objects.create(foodName = "Chicken Burger", price = 10, type = "Halal", cuisine = "Western", isDiscounted = True, discountRate = 20)

    
    @print_success
    def test_filterBy_minPrice(self):
        self.client.login(username="testuser", password = "password")

        response = self.client.get(reverse('filterFood'), {'min_price': 4})

        #print("Response Content:", response.content.decode())

         #check that food page is displayed
        self.assertEqual(response.status_code, 200)
        print(f"Response Status Code: {response.status_code}")

        self.assertEqual(len(response.context['filteredFood']), 3)
        print("Number of Filtered Food:",len(response.context['filteredFood']))

        self.assertTemplateUsed(response, "NTUFoodieApp/foodfilter.html")
        print("Templates used:", "NTUFoodieApp/foodfilter.html")

    
    @print_success
    def test_filterBy_maxPrice(self):
        self.client.login(username="testuser", password = "password")

        response = self.client.get(reverse('filterFood'), {'max_price': 10})

        #print("Response Content:", response.content.decode())

         #check that food page is displayed
        self.assertEqual(response.status_code, 200)
        print(f"Response Status Code: {response.status_code}")

        self.assertEqual(len(response.context['filteredFood']), 4)
        print("Number of Filtered Food:",len(response.context['filteredFood']))

        self.assertTemplateUsed(response, "NTUFoodieApp/foodfilter.html")
        print("Templates used:", "NTUFoodieApp/foodfilter.html")

    
    @print_success
    def test_filterBy_foodType(self):
        self.client.login(username="testuser", password = "password")

        response = self.client.get(reverse('filterFood'), {'type': 'Non-Halal'})

        #print("Response Content:", response.content.decode())

         #check that food page is displayed
        self.assertEqual(response.status_code, 200)
        print(f"Response Status Code: {response.status_code}")

        self.assertEqual(len(response.context['filteredFood']), 1)
        print("Number of Filtered Food:",len(response.context['filteredFood']))

        self.assertTemplateUsed(response, "NTUFoodieApp/foodfilter.html")
        print("Templates used:", "NTUFoodieApp/foodfilter.html")


    @print_success
    def test_filterBy_cuisine(self):
        self.client.login(username="testuser", password = "password")

        response = self.client.get(reverse('filterFood'), {'cuisine': 'Western'})

        #print("Response Content:", response.content.decode())

         #check that food page is displayed
        self.assertEqual(response.status_code, 200)
        print(f"Response Status Code: {response.status_code}")

        self.assertEqual(len(response.context['filteredFood']), 2)
        print("Number of Filtered Food:",len(response.context['filteredFood']))


        self.assertTemplateUsed(response, "NTUFoodieApp/foodfilter.html")
        print("Templates used:", "NTUFoodieApp/foodfilter.html")

    @print_success
    def test_filterBy_discountedFood(self):
        self.client.login(username="testuser", password = "password")

        response = self.client.get(reverse('filterFood'), {'discounted': 'true'})

        #print("Response Content:", response.content.decode())ls

         #check that food page is displayed
        self.assertEqual(response.status_code, 200)
        print(f"Response Status Code: {response.status_code}")

        self.assertEqual(len(response.context['filteredFood']), 2)
        print("Number of Filtered Food:",len(response.context['filteredFood']))


        self.assertTemplateUsed(response, "NTUFoodieApp/foodfilter.html")
        print("Templates used:", "NTUFoodieApp/foodfilter.html")

    
    @print_success
    def test_filterBy_combinedCriteria(self):
        self.client.login(username="testuser", password = "password")

        response = self.client.get(reverse('filterFood'), {'min_price': 3, 'max_price': 10, 'type': 'Halal', 'discounted': "true"})

        #print("Response Content:", response.content.decode())

         #check that food page is displayed
        self.assertEqual(response.status_code, 200)
        print(f"Response Status Code: {response.status_code}")

        self.assertEqual(len(response.context['filteredFood']), 2)
        print("Number of Filtered Food:",len(response.context['filteredFood']))


        self.assertTemplateUsed(response, "NTUFoodieApp/foodfilter.html")
        print("Templates used:", "NTUFoodieApp/foodfilter.html")


    

        
    

