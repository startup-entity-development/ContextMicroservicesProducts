from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from product_ctx_database_sqlalchemy_14.models.base import Base
from product_ctx_database_sqlalchemy_14.models import base as product_b
from product_ctx_database_sqlalchemy_14.models.category_model import ModelCategory
from product_ctx_database_sqlalchemy_14.models.sub_category_model import ModelSubCategory
from product_ctx_database_sqlalchemy_14.models.product_model import ModelProduct
from product_ctx_database_sqlalchemy_14.models.media_model import ModelMedia
from product_ctx_database_sqlalchemy_14.models.retailer_model import ModelRetailer
from product_ctx_database_sqlalchemy_14.models.retailer_location_model import ModelRetailerLocation

app = Flask(__name__)

app.config.from_object("config.StagingConfig")
db = SQLAlchemy(app, metadata=Base.metadata,
                model_class=Base,
                query_class=Base.query,
                )


migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run()
