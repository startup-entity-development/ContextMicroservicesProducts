from sqlalchemy_utils import database_exists, drop_database, create_database
import logging
import sys
from product_ctx_database_sqlalchemy_14.models import base as product_b
from product_ctx_database_sqlalchemy_14.models.category_model import ModelCategory
from product_ctx_database_sqlalchemy_14.models.sub_category_model import ModelSubCategory
from product_ctx_database_sqlalchemy_14.models.product_model import ModelProduct
from product_ctx_database_sqlalchemy_14.models.media_model import ModelMedia
#from product_ctx_database_sqlalchemy_14.models.retailer_model import ModelRetailer
#from product_ctx_database_sqlalchemy_14.models.product_retailer_model import ModelProductRetailer

# from order_ctx_database_sqlalchemy_14.models import base as order_b
# from order_ctx_database_sqlalchemy_14.models.cart import Cart
# from order_ctx_database_sqlalchemy_14.models.cart_product_detail import CartProductDetail
# from order_ctx_database_sqlalchemy_14.models.customer import Customer
# from order_ctx_database_sqlalchemy_14.models.shopper import Shopper
# from order_ctx_database_sqlalchemy_14.models.order import Order
# from order_ctx_database_sqlalchemy_14.models.status import Status
# from order_ctx_database_sqlalchemy_14.models.order_status import OrderStatus


# Load logging configuration
log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",)

def create_all_models(base_model, interactive: bool = False) -> None:
    log.info("Create models {}".format(base_model.db_name))
    log.info(f"create all models called interactive = {interactive}. ")

    if not database_exists(base_model.engine.url):
        create_database(base_model.engine.url)
    try:
        log.warning(f"Go ahead !")
        base_model.Base.metadata.create_all(base_model.engine)
        log.warning(f"all done!!!, and look good")
    except Exception as e:
        if database_exists(base_model.engine.url):
            try:
                if interactive is False:
                    raise Exception(
                        f" interactive option off.\n Trying to create database and tables,"
                        "but somethings go wrong.. error: {e} ")
                else:
                    a = input(
                        "Fail to create all models, drop database and retry ?, Yes = y, Cancel = c "
                    )
                    while a != "y" or a != "c":
                        if a == "y":
                            log.warning(f"Go ahead !")
                            drop_database(base_model.engine.url)
                            create_database(base_model.engine.url)
                            base_model.Base.metadata.create_all(base_model.engine)
                            log.warning(f"all done!!!, and look good")
                            return
                        if a == "c":
                            log.warning(f"Process canceled")
                        if a != "y" or "c":
                            log.warning(f"input option out the scope")

            except Exception as e:
                log.error(f"file: setup_db.py method:, create_all_models fail {e}")


if __name__ == "__main__":
    # base.Base.metadata.drop_all(base.engine)
    #create_all_models(order_b, interactive=True)
    create_all_models(product_b, interactive=True)
