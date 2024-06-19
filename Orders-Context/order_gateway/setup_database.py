from flask import jsonify
from sqlalchemy_utils import database_exists, drop_database, create_database
from sqlalchemy.engine import Engine
from order_ctx_database_sqlalchemy_14.models import base as b
from order_ctx_database_sqlalchemy_14.models.cart import ModelCart
from order_ctx_database_sqlalchemy_14.models.cart_product_detail import ModelCartProductDetail
from order_ctx_database_sqlalchemy_14.models.customer import ModelCustomer
from order_ctx_database_sqlalchemy_14.models.order import ModelOrder
from order_ctx_database_sqlalchemy_14.models.order_status import ModelOrderStatus
from order_ctx_database_sqlalchemy_14.models.shopper import ModelShopper
from order_ctx_database_sqlalchemy_14.models.status import ModelStatus
import logging
import sys

# Load logging configuration
log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",)

def reset_database(engine_url:str):
    log.warning("Resetting the database")
    drop_database(engine_url)
    create_database(engine_url)
    log.warning("Resetting the database done.")

def create_all_models(engine:Engine) -> str:
    log.info(f"Create all models start.")
    b.Base.metadata.create_all(engine)
    log.info(f"Create all models done.")

def message_all_done() -> str:
    msg_all_done = "Task completed! Everything looks good."
    log.warning(msg_all_done)
    return msg_all_done

def create_database_auth(interactive: bool = False) -> str:
    log.warning("----------------", b.engine.url)
    if not database_exists(b.engine.url):
        log.warning(f"Database does not exist, creating database.")
        create_database(b.engine.url)
    try:
        log.warning(f"Creating all models.")
        create_all_models(b.engine)
        msg : str = message_all_done()
        return jsonify(msg)
        
    except Exception as e:
        msg_input = "Unable to generate all models,"\
        " do you want to resetting the database"\
        "and attemptin the process again  ?,"\
        "Yes = y, Cancel = c :"\
        
        if database_exists(b.engine.url):
            try:
                if interactive is False:
                    log.warning(f"Unable to generate all models"
                                " resetting the database and attempting"
                                " the process again, error: {e}")
                    a = "y"
                else:
                    a = input( msg_input)
                    
                while a != "y" or a != "c":
                    if a == "y":
                        log.warning(f"Go ahead again !")
                        # reset_database(b.engine.url)
                        create_all_models(b.engine)
                        msg : str = message_all_done()
                        return jsonify(msg)
                    if a == "c":
                        log.warning("Process canceled")
                        return jsonify("Process canceled")
                    if a != "y" or "c":
                        log.warning(f"The input option is beyond the specified scope, please re-enter.")
                        a = input( msg_input)
                    
            except Exception as e:
                log.error(f"Failed to create models: {e}.")
                return  jsonify(f"Failed to create models: {e}.")
        
        else:
            log.error(f"Failed to create database {e}.")
            return  jsonify(f"Failed to create database: {e}.")

if __name__ == "__main__":
    log.info("Create models {}".format(b.db_name))
    create_database_auth(interactive=True)
