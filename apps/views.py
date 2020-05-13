from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser,FormParser, MultiPartParser
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import UserInfo, Student, Employee
from .serializers import EmployeeModelSerializer, EmployeeDeserializer


def user(request):
    print("请求到达")
    if request.method=="GET":
        print("GET")
        return HttpResponse("GET SUCCESS")
    elif request.method=="POST":
        print("POST")
        return HttpResponse("POST SUCCESS")
    elif request.method == "PUT":
        print("PUT 修改")
        return HttpResponse("PUT SUCCESS")
    elif request.method == "DELETE":
        print("DELETE 删除")
        return HttpResponse("DELETE SUCCESS")

@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):
    def get(self, request, *args, **kwargs):
        print("GET API")
        user_id = kwargs.get("pk")
        if user_id:
            # 查询单个
            user_values = UserInfo.objects.filter(pk=user_id).values("username", "password", "gender").first()
            if user_values:
                return Response({
                    "status": 200,
                    "message": "获取用户成功",
                    "results": user_values})
        else:
            user_list = UserInfo.objects.all().values("username", "password", "gender")
            if user_list:
                return Response({
                    "status": 201,
                    "message": "获取用户列表成功",
                    "results": list(user_list)
                })

        return Response({
            "status": 400,
            "message": "获取用户不存在",
        })

    def post(self, request, *args, **kwargs):
        """完成新增单个用户的操作"""
        print(request.POST)
        try:
            user_obj = UserInfo.objects.create(**request.POST.dict())
            if user_obj:
                return Response({
                    "status": 200,
                    "message": "新增用户成功",
                    "results": {"username": user_obj.username, "gender": user_obj.gender}
                })
            else:
                return Response({
                    "status": 500,
                    "message": "新增用户失败",
                })
        except:
            return Response({
                "status": 501,
                "message": "参数有误",
            })

    def put(self, request, *args, **kwargs):
        username = request.username
        password = request.password
        gender = request.gender
        user_id = kwargs.get("pk")
        user = UserInfo.objects.filter(pk=user_id).first()
        if user:
            user_obj = UserInfo.objects.create(username=username,password=password,gender=gender)
            if user_obj:
                return Response({
                    "status":200,
                    "message":"修改用户信息成功",
                    "results":{"username":user_obj.username,"password":user_obj.password,"gender":user_obj.gender}
                })
            else:
                return Response({
                    "status": 500,
                    "message": "修改用户信息失败"
                })
        else:
            return Response({
                "status":500,
                "message":"修改用户信息失败"
            })


    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        if user_id:
            user = UserInfo.objects.filter(pk=user_id).delete()
            return Response({
                "status": 200,
                "message": "删除用户成功"
            })
        else:
            return Response({
                "status": 500,
                "message": "删除用户信息失败"
            })

class StudentView(APIView):
    # renderer_classes = [BrowsableAPIRenderer]
    parser_classes = [JSONParser]
    # parser_classes = [MultiPartParser]
    # parser_classes = [FormParser]
    def get(self, request, *args, **kwargs):

        stu_id = kwargs.get("demo")

        # 如果 stu_id 存在  代表查询单个学生的信息
        if stu_id:
            # 如果获取的事queryset  则需要单独处理序列化
            # stu_obj = UserInfo.objects.filter(pk=stu_id).values("username", "gender").first()
            # 因为用户查询不到  get方法返回了系统无法处理的异常
            stu_obj = UserInfo.objects.get(pk=stu_id)
            # 如果有值  代表查询成功
            if stu_obj:
                return Response({
                    "status": 200,
                    "message": "GET USER SUCCESS",
                    "results": stu_obj,
                })
            else:
                # 代表查询的用户信息不存在
                return Response({
                    "status": 403,
                    "message": "查询的用户不存在",
                })
        # id如果不存在  代表查询的是全部的用户信息
        else:
            stu_val = UserInfo.objects.all().values("username", "password", "gender")
            return Response({
                "status": 200,
                "message": "查询所有用户成功",
                "results": list(stu_val)
            })

    def post(self,request,*args,**kwargs):
        print(request.POST.dict())
        try:
            stu_obj = UserInfo.objects.create(**request.POST.dict())
            if stu_obj:
                return Response({
                    "status": 200,
                    "message": "添加学生成功",
                    "results":{
                        "username":stu_obj.username,
                        "password":stu_obj.password
                    }
                })
            else:
                return Response({
                    "status": 500,
                    "message": "添加学生失败"
                })
        except:
            return Response({
                "status": 501,
                "message": "参数有误"
            })
class EmployeeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        emp_id = kwargs.get("id")

        if emp_id:
            try:
                emp_obj = Employee.objects.get(pk=emp_id)
                # print(emp_obj, type(emp_obj))
                emp_ser = EmployeeModelSerializer(emp_obj).data
                return Response({
                    "status": 200,
                    "message": "用户查询成功",
                    "results": emp_ser,
                })
            except:
                return Response({
                    "status": 500,
                    "message": "用户不存在"
                })
        # 查询全部
        else:
            emp_list = Employee.objects.all()
            emp_ser = EmployeeModelSerializer(emp_list, many=True).data
            return Response({
                "status": 200,
                "message": "用户列表查询成功",
                "results": emp_ser,
            })
    def post(self, request, *args, **kwargs):
        request_data = request.data
        if not isinstance(request_data, dict) or request_data == {}:
            return Response({
                "status": 500,
                "message": "数据有误"
            })

        deserializer = EmployeeDeserializer(data=request_data)
        print(deserializer)
        if deserializer.is_valid():
            emp_obj = deserializer.save()
            print(emp_obj)
            return Response({
                "status": 200,
                "message": "用户创建成功",
                "results": EmployeeModelSerializer(emp_obj).data
            })
        else:
            return Response({
                "status": 500,
                "message": "用户创建失败",
                "results": deserializer.errors
            })