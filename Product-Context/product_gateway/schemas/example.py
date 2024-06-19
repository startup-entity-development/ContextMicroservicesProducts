# from graphene_sqlalchemy import SQLAlchemyObjectType

# class ActiveSQLAlchemyObjectType(SQLAlchemyObjectType):
#     class Meta:
#         abstract = True

#     @classmethod
#     def get_node(cls, info, id):
#         return cls.get_query(info).filter(
#             and_(cls._meta.model.deleted_at==None,
#                  cls._meta.model.id==id)
#             ).first()

# class User(ActiveSQLAlchemyObjectType):
#     class Meta:
#         model = UserModel

# class Query(graphene.ObjectType):
#     users = graphene.List(User)

#     def resolve_users(self, info):
#         query = User.get_query(info)  # SQLAlchemy query
#         return query.all()

# schema = graphene.Schema(query=Query)