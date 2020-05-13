from rest_framework import serializers, exceptions

from apps.models import Employee
from day1 import settings


class EmployeeModelSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    gender=serializers.IntegerField()
    pic=serializers.ImageField()
    example=serializers.SerializerMethodField()
    def get_example(self,obj):
        return "example"

    gender=serializers.SerializerMethodField()
    def get_gender(self,obj):
        # if obj.gender==0:
        #     return "男"
        # elif obj.gender==1:
        #     return "女"
        # return "未知"
        return obj.get_gender_display()

    pic = serializers.SerializerMethodField()

    def get_pic(self, obj):
        print(type(obj.pic))
        print("http://127.0.0.1:8000" + settings.MEDIA_ROOT + str(obj.pic))
        return "%s%s%s" % ("http://127.0.0.1:8000", settings.MEDIA_ROOT, str(obj.pic))

class EmployeeDeserializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=10,
        min_length=5,
        error_messages={
            "max_length": "太长",
            "min_length": "太短"
        }
    )
    password = serializers.CharField()
    phone = serializers.CharField(required=False)
    re_pwd = serializers.CharField()

    # 局部校验钩子
    def validate_username(self, value):
        if "1" in value:
            raise exceptions.ValidationError("用户名异常")
        return value

    # 全局的校验钩子
    def validate(self, attrs):
        print(attrs, "attr")
        password = attrs.get("password")
        re_pwd = attrs.pop("re_pwd")
        if password != re_pwd:
            raise exceptions.ValidationError("两次密码不一致")
        return attrs

    def create(self, validated_data):
        print(validated_data)
        return Employee.objects.create(**validated_data)