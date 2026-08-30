from rest_framework import serializers

from PIL import Image

from .models import Product, ProductImage


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'price', 'created_at', 'updated_at', 'is_published')
        read_only_fields = ('created_at', 'updated_at')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('product', 'image', 'created_at', 'is_published')
        read_only_fields = ('created_at')

    def validate_image(self, value):
        # 1. Проверка размера файла
        max_size_mb = 5
        if value.size > max_size_mb * 1024 * 1024:
            raise serializers.ValidationError(
                f"Файл слишком большой. Максимум {max_size_mb} МБ."
            )

        # 2. Проверка формата
        valid_extensions = ['jpg', 'jpeg', 'png']
        ext = value.name.split('.')[-1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError(
                f"Недопустимый формат. Разрешены: {', '.join(valid_extensions)}."
            )

        # 3. Проверка разрешения изображения
        image = Image.open(value)
        max_width, max_height = 4000, 4000
        if image.width > max_width or image.height > max_height:
            raise serializers.ValidationError(
                f"Разрешение изображения не должно превышать {max_width}x{max_height}px."
            )

        return value