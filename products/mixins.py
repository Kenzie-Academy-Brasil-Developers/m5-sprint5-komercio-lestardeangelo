class SerializerByMethodMixin:
    def get_serializer_class(self):
        return self.serializer_map.get(self.request.method, self.serializer_class)