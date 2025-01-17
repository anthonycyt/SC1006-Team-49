from django.test import TestCase, Client
from NTUFoodieApp.models import *
from django.contrib.auth.models import User
from django.urls import reverse

# Helper decorator to print success message after each test with formatting
def print_success(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        print(f"{'-'*10} {func.__name__} passed successfully {'-'*10}\n")
    return wrapper

# Test Models (White Box Testing)
class BaseTestData(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password="password")

        cls.consumer = Consumer.objects.create(
            user=cls.user,
            firstName='Jane',
            lastName='Tan',
            email="jane.tan@gmail.com",
            profilePic="default_profile.png",
        )
        cls.location = Location.objects.create(
            canteenName="Canteen 20",
            address="Opp Hall 19 Bus Stop",
        )
        cls.canteen = Canteen.objects.create(
            location=cls.location
        )
        cls.store = Store.objects.create(
            storeName="Korean Store",
            canteen=cls.canteen,
        )

class ConsumerModelTest(BaseTestData):
    @print_success
    def test_consumer_creation(self):
        self.assertIsInstance(self.consumer, Consumer)  # Test if Consumer instance is created
        print("\nConsumer instance created successfully.")

    @print_success
    def test_consumer_str_display(self):
        expected_output = "Jane Tan"
        self.assertEqual(str(self.consumer), expected_output)
        print(f"Consumer string representation: {str(self.consumer)}")

class LocationModelTest(BaseTestData):
    @print_success
    def test_location_creation(self):
        self.assertIsInstance(self.location, Location)
        self.assertEqual(self.location.canteenName, "Canteen 20")
        self.assertEqual(self.location.address, "Opp Hall 19 Bus Stop")
        print("Location instance created successfully with canteenName and address.")

    @print_success
    def test_location_address_display(self):
        expected_output = "Opp Hall 19 Bus Stop"
        self.assertEqual(str(self.location), expected_output)
        print(f"Location string representation: {str(self.location)}")

class CanteenModelTest(BaseTestData):
    @print_success
    def test_canteen_creation(self):
        self.assertIsInstance(self.canteen, Canteen)  # Test if Canteen instance is created
        print("Canteen instance created successfully.")

    @print_success
    def test_canteen_str_display(self):
        expected_output = "Canteen 20"
        self.assertEqual(str(self.canteen.location.canteenName), expected_output)
        print(f"Canteen string representation: {str(self.canteen.location.canteenName)}")

class StoreModelTest(BaseTestData):
    @print_success
    def test_store_creation(self):
        self.assertIsInstance(self.store, Store)
        self.assertEqual(self.store.storeName, "Korean Store")
        self.assertEqual(self.store.canteen, self.canteen)
        print("Store instance created successfully with storeName and canteen.")

    @print_success
    def test_store_str_display(self):
        expected_output = "Korean Store @ Canteen 20"
        self.assertEqual(str(self.store), expected_output)
        print(f"Store string representation: {str(self.store)}")

class StoreOwnerModelTest(BaseTestData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = User.objects.create_user(username='storeownertest', password="password")
        cls.storeOwner = StoreOwner.objects.create(
            user=cls.user,
            store=cls.store,
            firstName="store",
            lastName="owner",
            email="storeownertest@gmail.com",
            profilePic="default_profile.png",
        )
    
    @print_success
    def test_storeOwner_creation(self):
        self.assertIsInstance(self.storeOwner, StoreOwner)
        self.assertEqual(self.storeOwner.user, self.user)
        self.assertEqual(self.storeOwner.store, self.store)
        self.assertEqual(self.storeOwner.firstName, "store")
        self.assertEqual(self.storeOwner.lastName, "owner")
        print("StoreOwner instance created successfully with user, store, firstName, and lastName.")

    @print_success
    def test_storeOwner_str_display(self):
        expected_output = "store owner"
        self.assertEqual(str(self.storeOwner), expected_output)
        print(f"StoreOwner string representation: {str(self.storeOwner)}")

class FoodModelTest(BaseTestData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.food = Food.objects.create(
            store=cls.store,
            foodName="Japchae",
            price=5.50,
            type="Non-Halal",
            cuisine="Korean",
            description="Delicious Japchae",
            rating=4.5,
            isDiscounted=True,
            discountRate=10,
        )
    
    @print_success
    def test_food_creation(self):
        self.assertIsInstance(self.food, Food)
        self.assertEqual(self.food.store.storeName, self.store.storeName)
        self.assertEqual(self.food.store.canteen.location.canteenName, self.store.canteen.location.canteenName)
        self.assertEqual(self.food.foodName, "Japchae")
        print("Food instance created successfully with foodName, store, and canteen information.")

    @print_success
    def test_food_str_display(self):
        expected_output = "Japchae from Korean Store @ Canteen 20"
        self.assertEqual(str(self.food), expected_output)
        print(f"Food string representation: {str(self.food)}")

    @print_success
    def test_discountedPrice_calculation(self):
        expected_discountedPrice = self.food.price * ((100 - self.food.discountRate) / 100)
        self.food.refresh_from_db()  # Refresh the instance from the database to ensure the latest data is loaded after save
        self.assertEqual(self.food.discountedPrice, expected_discountedPrice)
        print(f"Discounted price calculated correctly: {self.food.discountedPrice}")

class ReviewModelTest(BaseTestData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.food = Food.objects.create(foodName="Ddukbokki", store=cls.store)

        cls.review = Review.objects.create( 
            user=cls.user,
            food=cls.food,
            rating=4.5,
            description="Great taste!",
        )
    
    @print_success
    def test_review_creation(self):
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.food, self.food)
        self.assertEqual(self.review.rating, 4.5)
        self.assertEqual(self.review.description, "Great taste!")
        print("Review instance created successfully with user, food, rating, and description.")

    @print_success
    def test_review_str_display(self):
        expected_output = "Jane Tan , Ddukbokki from Korean Store"
        self.assertEqual(str(self.review), expected_output)
        print(f"Review string representation: {str(self.review)}")

    @print_success
    def test_valid_rating_creation(self):
        review = Review.objects.create(user=self.user, food=self.food, rating=5.0, description="Good")
        self.assertEqual(review.rating, 5.0)
        print("Review instance created with a valid rating of 5.0.")

    @print_success
    def test_same_name_reviews(self):
        Review.objects.create(user=self.user, food=self.food, rating=4.5)
        Review.objects.create(user=self.user, food=self.food, rating=3.0)
        self.assertEqual(self.food.reviews.count(), 3)
        print("Multiple reviews with the same food and user names were created successfully.")

class FlaggedReviewModelTest(BaseTestData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.flaggingUser = User.objects.create_user(username='john', password="password")
        cls.food = Food.objects.create(foodName="Bulgogi", store=cls.store)
        cls.review = Review.objects.create(
            user=cls.user,
            food=cls.food,
            rating=2.0,
            description="Tasteless...",
        )

        cls.flaggedReview = FlaggedReview.objects.create(
            review=cls.review,
            flaggedBy=cls.flaggingUser,
            reason="Inappropriate Review",
        )
    
    @print_success
    def test_flaggedReview_creation(self):
        self.assertIsInstance(self.flaggedReview, FlaggedReview)
        self.assertEqual(self.flaggedReview.review, self.review)
        self.assertEqual(self.flaggedReview.flaggedBy, self.flaggingUser)
        self.assertEqual(self.flaggedReview.reason, "Inappropriate Review")
        print("FlaggedReview instance created successfully with review, flaggedBy, and reason.")

    @print_success
    def test_default_isProcessed(self):
        self.assertFalse(self.flaggedReview.isProcessed)
        print("isProcessed default value is False.")

    @print_success
    def test_flaggedReview_str_display(self):
        expected_output = f"Review {self.review} flagged by {self.flaggingUser}"
        self.assertEqual(str(self.flaggedReview), expected_output)
        print(f"FlaggedReview string representation: {str(self.flaggedReview)}")

class NotificationModelTest(BaseTestData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.notification = Notification.objects.create(
            title="Hello",
            description="Nice to see you",
            user=cls.user,
        )
    
    @print_success
    def test_notification_creation(self):
        self.assertIsInstance(self.notification, Notification)
        self.assertEqual(self.notification.title, "Hello")
        self.assertEqual(self.notification.description, "Nice to see you")
        self.assertEqual(self.notification.user, self.user)
        print("Notification instance created successfully with title, description, and user.")

    @print_success
    def test_notification_defaultViewed(self):
        self.assertFalse(self.notification.viewed)  # viewed should default to False
        print("Viewed default value is False.")

    @print_success
    def test_notification_str_display(self):
        expected_output = "Notification for testuser. Title: Hello"
        self.assertEqual(str(self.notification), expected_output)
        print(f"Notification string representation: {str(self.notification)}")

class BannedUserModelTest(BaseTestData):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.banUser = User.objects.create_user(username='test', password="password")
        cls.bannedUser = BannedUser.objects.create(
            user=cls.banUser,
        )
    
    @print_success
    def test_bannedUser_creation(self):
        self.assertIsInstance(self.bannedUser, BannedUser)
        self.assertEqual(self.bannedUser.user, self.banUser)
        print("BannedUser instance created successfully with user.")

    @print_success
    def test_bannedUser_isBanned(self):
        self.assertTrue(self.bannedUser.isBanned)
        print("isBanned default value is True.")

    @print_success
    def test_bannedUser_str_display(self):
        expected_output = "Banned user: test."
        self.assertEqual(str(self.bannedUser), expected_output)
        print(f"BannedUser string representation: {str(self.bannedUser)}")
