from flask import jsonify
from sqlalchemy_utils import database_exists, drop_database, create_database
import logging
import sys
from pricing_ctx_database_sqlalchemy_14.models import base as b
from pricing_ctx_database_sqlalchemy_14.models.model_weight_delivery import ModelWeightDelivery
from pricing_ctx_database_sqlalchemy_14.models.model_pricing_account import ModelPricingAccount
from pricing_ctx_database_sqlalchemy_14.models.model_pricing_profile import ModelPricingProfile
from pricing_ctx_database_sqlalchemy_14.models.model_account_promotion import ModelAccountPromotion
from sqlalchemy.engine import Engine

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
    log.info("Create all models start.")
    b.Base.metadata.create_all(engine)
    log.info("Create all models done.")

def message_all_done() -> str:
    msg_all_done = "Task completed! Everything looks good."
    log.warning(msg_all_done)
    return msg_all_done

def create_database_pricing(interactive: bool = False) -> str:
    """
    Creates a pricing database if it does not exist, then generates all models 
    and returns a message indicating completion. If an error occurs, it provides 
    options to reset the database and attempt the process again, or cancels the 
    process. Returns messages indicating success or failure.
    
    Parameters:
    - interactive: a bool indicating whether the process should be interactive
    
    Returns:
    - str: a message indicating completion or failure
    """
    if not database_exists(b.engine.url):
        log.warning("Database does not exist, creating database.")
        create_database(b.engine.url)
    try:
        log.warning("Creating all models.")
        create_all_models(b.engine)
        msg : str = message_all_done()
        if interactive:
            return msg
        return jsonify(msg)
        
    except Exception as e:
        msg_input = "Unable to generate all models,"\
        " do you want to resetting the database"\
        "and attempting the process again  ?,"\
        "Yes = y, Cancel = c :"\
        
        if database_exists(b.engine.url):
            try:
                if interactive is False:
                    log.warning("Unable to generate all models"
                                " resetting the database and attempting"
                                " the process again, error: {e}")
                    a = "y"
                else:
                    a = input( msg_input)
                    
                while a != "y" or a != "c":
                    if a == "y":
                        log.warning("Go ahead again !")
                        reset_database(b.engine.url)
                        create_all_models(b.engine)
                        msg : str = message_all_done()
                        if interactive:
                            return msg
                        return jsonify(msg)
                    if a == "c":
                        log.warning("Process canceled")
                        if interactive:
                            return "Process canceled"
                        return jsonify("Process canceled")
                    if a != "y" or "c":
                        log.warning("The input option is beyond the specified scope, please re-enter.")
                        a = input( msg_input)
                    
            except Exception as e:
                log.error(f"Failed to create models: {e}.")
                if interactive:
                    return "Failed to create models"
                return  jsonify(f"Failed to create models: {e}.")
        
        else:
            log.error(f"Failed to create database {e}.")
            if interactive:
                return "Failed to create database"
            return  jsonify(f"Failed to create database: {e}.")


        
if __name__ == "__main__":
    log.info("Create models {}".format(b.db_name))
    create_database_pricing(interactive=True)
