# ./main.py
# localhost:8000/pyn/api/money/list
# localhost:8000/pyn/api/money/create
# localhost:8000/pyn/api/money/update  body {id:111,name:111}
# localhost:8000/pyn/api/money/delete


# get post

# @app.get localhost:8000/pyn/api/moneys
# @app.post localhost:8000/pyn/api/money
# @app.put localhost:8000/pyn/api/money/6666 body{name:111}
# @app.delete localhost:8000/pyn/api/money/6666

from ast import Add
import datetime
import json
from typing import ItemsView
from models import Users, Records
from tortoise.contrib.sanic import register_tortoise
from sanic import Sanic, response
from sanic.response import HTTPResponse, text
from sanic.request import Request
from sanic_openapi import doc, openapi2_blueprint
# http://0.0.0.0:8000/swagger/

app = Sanic(__name__)
app.blueprint(openapi2_blueprint)

register_tortoise(
    app, db_url="mysql://cyh:Bulai0408!@rm-uf6kv8scizjoc6gw1go.mysql.rds.aliyuncs.com:3306/bill", modules={"models": ["models"]}, generate_schemas=True
)

#  Select all list


@app.get("/record/list")
async def get_record_list(request):
    records = await Records.all()
    array = []
    for i in records:
        i = dict(i)
        i['created_at'] = i['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        i['updated_at'] = i['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
        array.append(i)
    array.sort(key=lambda k: (k.get('created_at', 0)), reverse=True)
    print(array)
    data = {"data": array}

    return response.json(data)


@app.post("/record/create")
# for swagger, the same with your needed params
@doc.consumes(doc.JsonBody({
    "name": str,
    "price": int,
    "type": int
}), location='body')
async def create_new_record(request):
    data = request.json
    name_add = data["name"]
    type_add = int(data["type"])
    price_add = data["price"]
    user_info = await Records.create(name=name_add, type=type_add, price=price_add)

    user_info_dict = dict(user_info)

    user_info_dict['created_at'] = user_info_dict['created_at'].strftime(
        "%Y-%m-%d %H:%M:%S")
    user_info_dict['updated_at'] = user_info_dict['updated_at'].strftime(
        "%Y-%m-%d %H:%M:%S")

    return response.json({
        "code": 200,
        "message": "Add Items Succeed!",
        "data": user_info_dict
    })


@app.post("/record/update")
# for swagger, the same with your needed params
@doc.consumes(doc.JsonBody({
    "id": int,
    "name": str,
    "price": int,
    "type": int
}), location='body')
async def update_record(request):
    data = request.json
    id = data["id"]

    # 第一个参数 一个 dict eg:{"key1":1,"key2":2,"key3":3}
    # 第二个参数 要去除的key eg:{"key1","key2"}
    # 得到 {"key3":3}
    def without_keys(d, keys):
        return {k: v for k, v in d.items() if k not in keys}

    omit_id_data = without_keys(data, {"id"})

    user_info = await Records.filter(id=id).update(**omit_id_data)
    return response.json({
        "code": 200,
        "message": "Updated Items Succeed!",
        "data": user_info
    })


@app.post("/record/delete")
# for swagger, the same with your needed params
@doc.consumes(doc.JsonBody({
    "id": int
}), location='body')
async def delete_one_record(request):
    data = request.json
    id_delete = int(data["id"])

    user_info = await Records.get(id=id_delete)
    user_info_dict = dict(user_info)
    user_info_dict['created_at'] = user_info_dict['created_at'].strftime(
        "%Y-%m-%d %H:%M:%S")
    user_info_dict['updated_at'] = user_info_dict['updated_at'].strftime(
        "%Y-%m-%d %H:%M:%S")

    await user_info.delete()

    return response.json(
        {
            "code": 200,
            "message": "Delete Items Succeed!",
            "Deleted data": user_info_dict
        }
    )


# @app.post("/user/<user:str>")
# async def add_user(request , user):
#     user_info = await Users.create(name = user)
#     if user_info is not None:
#         # user_query = await Users.filter(name__contains='Yuna').first()
#         return response.json({
#             "code":200,
#             "message":"Add user successed!",
#             "user":dict(user_info)
#         })
#     else:
#         return response.json({
#             "code":502,
#             "message":"Server Error!",
#             "user": None
#         })


# @app.post("/user")
# async def add_user(request):
#     data = request.json
#     user=data['user']
#     print(user)
#     user_info = await Users.create(name = user)
#     if user_info is not None:
#         # user_query = await Users.filter(name__contains='Yuna').first()
#         return response.json({
#             "code":200,
#             "message":"Add user successed!",
#             "user":dict(user_info)
#         })
#     else:
#         return response.json({
#             "code":502,
#             "message":"Server Error!",
#             "user": None
#         })


# @app.post("/user/create")
# async def add_user(request):
    # data = request.json
    # user=data['user']
    # print(user)
    # user_info = await Users.create(name = user)
    # if user_info is not None:
    #     # user_query = await Users.filter(name__contains='Yuna').first()
    #     return response.json({
    #         "code":200,
    #         "message":"Add user successed!",
    #         "user":dict(user_info)
    #     })
    # else:
    #     return response.json({
    #         "code":502,
    #         "message":"Server Error!",
    #         "user": None
    #     })

# @app.post("/user/delete")
# async def add_user(request):
    # data = request.json
    # user=data['user']
    # print(user)
    # user_info = await Users.create(name = user)
    # if user_info is not None:
    #     # user_query = await Users.filter(name__contains='Yuna').first()
    #     return response.json({
    #         "code":200,
    #         "message":"Add user successed!",
    #         "user":dict(user_info)
    #     })
    # else:
    #     return response.json({
    #         "code":502,
    #         "message":"Server Error!",
    #         "user": None
    #     })

@app.delete("/user")
async def delete_user(request):
    await Users.delete(id=id)


("/user")


async def list_all(request):
    users = await Users.all()
    return response.json({"users": [str(user) for user in users]})


# @app.route("/user/<pk:int>")
# async def get_user(request, pk):
#     user = await Users.query(pk=pk)
#     return response.json({"user": str(user)})


if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0")
