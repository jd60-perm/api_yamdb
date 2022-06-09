from rest_framework import mixins, viewsets


class PostListDelMixin(
    mixins.DestroyModelMixin, mixins.ListModelMixin,
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    pass
