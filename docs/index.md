# 📅 A To-do List in a Calendar

This project is my first try to create an organized application, with documentation and good pratices. I've applied in this API concepts about clean code, RESTful API, PEP8 and PEP257.

## Hosting

I've hosted this project in render.com, because it's free and no need credit card. It's can be access in: <https://todo365.onrender.com/api/>

## DRF Swagger

Using drf-yasg I've created a swagger explaining any types of possible requests.

## Diagrams

Here are all the project diagrams, I tried to explain their functionalities and relationships.

### Models and Serializers Class Diagrams

```mermaid
classDiagram
    
    User <|-- UserSerializer : inheritance
    User o-- "0..*" Task : create
    Task <|-- TaskSerializer : inheritance
    
    note for User "This class have a inheritance in AbstractUser from django.contrib.auth.models"

    class User{
        # user_email: EmailField
        # validated: BooleanField default=False
        # tasks: dict ~task objects~
        + __str__() str
    }
    class Task{
        # title: CharField
        # description: CharField
        # datetime: DatetimeField
        # ForeignKey(User) IntegerField
        + __str__() string
    }
    class TaskSerializer{
        - Meta
        + validate_datetime(value) ValidationError
    }
    class UserSerializer{
        + create(validated_data) User
    }
```

### Custom Permission Class Diagram

```mermaid
classDiagram

    direction RL
    
    note for IsAdmin "inheritance in BasePermission"

    class IsAdmin{
        # has_permission() bool
    }
```

### Views Class Diagrams

```mermaid
classDiagram

    note for HealthCheckView "inheritance in generics.ListAPIView"

    class HealthCheckView{
        - get() dict ~status~
    }
```

```mermaid
classDiagram

    note for TaskDetail "inheritance in generics.RetrieveUpdateDestroyAPIView"

    class TaskDetail{
        - serializer_class: TaskSerialiazer
        - permission_classes: list ~permissions~
        - get_queryset() Task object
    }
```

```mermaid
classDiagram

    note for TaskList "inheritance in generics.ListCreateAPIView"
    
    class TaskList{
        - serializer_class: TaskSerialiazer
        - permission_classes: list ~permissions~
        - get_queryset() Task objects
        - perform_create() Task serializer save
    }
```

```mermaid
classDiagram

    BaseUserCreate <|-- UserCreate : inheritance
    BaseUserCreate <|-- UserAdminCreate : inheritance

    note for BaseUserCreate "inheritance in generics.CreateAPIView"

    class BaseUserCreate{
        # serializer_class: UserSerialiazer
        # queryset: User objects
        # perform_create() User serializer save
    }
    class UserCreate{
        - perform_create() User serializer save
    }
    class UserAdminCreate{
        -perform_create() User serializer save
    }
```

```mermaid
classDiagram

    note for UserList "inheritance in generics.ListAPIView"
    
    class UserList{
        - serializer_class: UserSerialiazer
        - permission_classes: list ~permissions~
        - get_queryset() User objects
    }
```

```mermaid
classDiagram

    note for UserDetailAdmin "inheritance in generics.RetrieveUpdateDestroyAPIView"
    
    class UserDetailAdmin{
        - serializer_class: UserSerialiazer
        - permission_classes: list ~permissions~
        - queryset: User objects
    }
```

```mermaid
classDiagram

    note for UserDetail "inheritance in generics.RetrieveUpdateAPIView"
    
    class UserDetail{
        - serializer_class: UserSerialiazer
        - queryset: User objects
        - get_object() self User
    }
```

```mermaid
classDiagram

    note for VerifyEmailToken "inheritance in rest_framework.views.APIView"
    
    class VerifyEmailToken{
        - serializer_class: UserSerialiazer
        - get serializer.data
    }
```
