from email.mime import image
from django.db.models.expressions import F
from ..models.kits_models import Kit,KitCategory, KitImages
from rest_framework import serializers


class KitCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = KitCategory
        fields = '__all__'


class KitDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kit
        fields = '__all__'
        depth = 2


class KitSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.CharField()
    # category = serializers.PrimaryKeyRelatedField(queryset=KitCategory.objects.all())
    category = KitCategorySerializer(many=False,read_only=True)
    stock = serializers.IntegerField()
    active = serializers.BooleanField(default=True)
    image_1 = serializers.ImageField(required=True)
    image_2 = serializers.ImageField(required=True)
    image_3 = serializers.ImageField(required=True)
    image_4 = serializers.ImageField(required=True)
    # category = serializers.IntegerField()
    # images = serializers.SerializerMethodField()
    # class Meta:
    #     model = Kit
    #     fields = ['name','description','price','category','stock','active','image_1','image_2','image_3','image_4']
        # depth = 2

    # def get_images(self,obj):
    #     return KitImages.objects.filter(kit=obj.id).values('image').distinct()


class CreateKitSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.CharField()
    # category = serializers.PrimaryKeyRelatedField(queryset=KitCategory.objects.all())
    category = serializers.IntegerField()
    stock = serializers.IntegerField()
    active = serializers.BooleanField(default=True)
    image_1 = serializers.ImageField(required=True)
    image_2 = serializers.ImageField(required=True)
    image_3 = serializers.ImageField(required=True)
    image_4 = serializers.ImageField(required=True)


class GetKitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kit
        fields = '__all__'
        depth = 2


class AddKitCategorySerializer(serializers.Serializer):
    name = serializers.CharField()
    image = serializers.ImageField(required=True)


class UpdateKitSerializer(serializers.ModelSerializer):
    image_1 = serializers.ImageField(max_length=None, use_url=True,required=False)
    image_2 = serializers.ImageField(max_length=None, use_url=True,required=False)
    image_3 = serializers.ImageField(max_length=None, use_url=True,required=False)
    image_4 = serializers.ImageField(max_length=None, use_url=True,required=False)
    # category = serializers.IntegerField()
    class Meta:
        model = Kit
        # fields = '__all__'
        fields = ['name','category','description','price','image_1','image_2','image_3','image_4','stock','active']
        extra_kwargs = {
            'name': {'required': False},
            'category': {'required': False},
            'description': {'required': False},
            'price': {'required': False},
            'image_1': {'required': False},
            'image_2': {'required': False},
            'image_3': {'required': False},
            'image_4': {'required': False},
            'stock': {'required': False},
            'active': {'required': False},
        }
   