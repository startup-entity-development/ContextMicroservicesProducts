from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pricing_ctx_database_sqlalchemy_14.models.base import Base
from pricing_ctx_database_sqlalchemy_14.models.model_weight_delivery import ModelWeightDelivery
from pricing_ctx_database_sqlalchemy_14.models.model_account_promotion import ModelAccountPromotion
from pricing_ctx_database_sqlalchemy_14.models.model_pricing_account import ModelPricingAccount
from pricing_ctx_database_sqlalchemy_14.models.model_pricing_profile import ModelPricingProfile


app = Flask(__name__)

app.config.from_object("config.StagingConfig")
db = SQLAlchemy(app, metadata=Base.metadata,
                model_class=Base,
                query_class=Base.query,
                )


migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run()
