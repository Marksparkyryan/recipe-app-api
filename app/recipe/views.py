from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe import serializers


class BaseIngredientBaseTagViewset(viewsets.GenericViewSet,
                                   mixins.ListModelMixin,
                                   mixins.CreateModelMixin):
    """Base viewset for Receipes and Tags"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseIngredientBaseTagViewset):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseIngredientBaseTagViewset):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Create, retrieve, update, destroy, list recipe objects"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Limit objects to authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return serializer that specializes in handling related field
        data instead of just related keys as this views default
        serializer does.
        """
        # action is lowercase
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        return self.serializer_class
