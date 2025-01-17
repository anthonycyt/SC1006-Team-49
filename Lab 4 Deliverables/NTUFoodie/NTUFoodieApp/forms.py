from django.forms import ModelForm
from .models import Review
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class ConsumerForm(ModelForm):
    class Meta:
        model = Consumer
        fields = ['firstName', 'lastName', 'profilePic']
        widgets = {
            'profilePic': forms.FileInput()
        }
        
class StoreOwnerForm(ModelForm):
    class Meta:
        model = StoreOwner
        fields = ['firstName', 'lastName', 'profilePic']
        widgets = {
            'profilePic': forms.FileInput()
        }

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'description', 'image']
        
class FlagReviewForm(ModelForm):
    class Meta:
        model = FlaggedReview
        fields = ['reason']
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
from django import forms
from .models import Food

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['foodName', 'price', 'type', 'cuisine', 'description', 'isDiscounted', 'discountRate', 'image']

    def __init__(self, *args, **kwargs):
        super(FoodForm, self).__init__(*args, **kwargs)
        # Set choices for 'type' and 'cuisine' dynamically
        self.fields['type'].widget = forms.Select(
            choices=[(type_choice, type_choice) for type_choice in Food.objects.values_list('type', flat=True).distinct()]
        )
        self.fields['cuisine'].widget = forms.Select(
            choices=[(cuisine_choice, cuisine_choice) for cuisine_choice in Food.objects.values_list('cuisine', flat=True).distinct()]
        )
        
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Price cannot be negative.')
        return price

    def clean(self):
        cleaned_data = super().clean()
        is_discounted = cleaned_data.get('isDiscounted')
        discount_rate = cleaned_data.get('discountRate')

        # Validate discountRate only if isDiscounted is True
        if is_discounted:
            if discount_rate is None:
                self.add_error('discountRate', 'Please provide a discount rate when the item is discounted.')
            else:
                if discount_rate < 0:
                    self.add_error('discountRate', 'Discount rate cannot be negative.')
                elif discount_rate >= 100:
                    self.add_error('discountRate', 'Discount rate must be less than 100%.')
        else:
            # If the item is not discounted, ensure discountRate is None
            cleaned_data['discountRate'] = None
        return cleaned_data