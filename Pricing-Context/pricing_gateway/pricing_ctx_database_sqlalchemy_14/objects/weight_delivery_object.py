from pricing_ctx_database_sqlalchemy_14.models.model_weight_delivery import ModelWeightDelivery
from pricing_ctx_database_sqlalchemy_14.objects.abstract_object import ObjectDataBase


class WeightDeliveryDataBase(ObjectDataBase):
    
    def __init__(self, db_session, log):
        self.log = log
        self.db_session = db_session
        super().__init__(db_session, log)

    def create(self,auto_commit :bool=True, **kwargs) -> None:
        try:
            weight_delivery = self.model(**kwargs)
            self.db_session.add(weight_delivery)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: weight_delivery_object.py method: create fail {e}")
            raise e
    
    def get(self, id:int) -> ModelWeightDelivery:
        try:
            weight_delivery = self.db_session.query(ModelWeightDelivery).get(id)
            return weight_delivery
        except Exception as e:
            self.log.error(f"file: weight_delivery_object.py method: get fail {e}")
            raise e
    
    
    def get_all(self) -> list[ModelWeightDelivery]:
        try:
            weight_delivery = self.db_session.query(ModelWeightDelivery).all()
            return weight_delivery
        except Exception as e:
            self.log.error(f"file: weight_delivery_object.py method: get_all fail {e}")
            raise e
    
    def delete(self, id:int, auto_commit:bool= True) -> None:
        try:
            weight_delivery = self.get(id)
            self.db_session.delete(weight_delivery)
            if auto_commit:
                self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: weight_delivery_object.py method: delete fail {e}")
            raise e
        
    def update(self, id:int, auto_commit:bool= True, **kwargs) -> None:
        try:
            weight_delivery = self.get(id)
            for key, value in kwargs.items():
                setattr(weight_delivery, key, value)
            if auto_commit:
                self.db_session.commit()
            else:
                self.db_session.flush()
            self.db_session.refresh(weight_delivery)
        except Exception as e:
            self.db_session.rollback()
            self.log.error(f"file: weight_delivery_object.py method: update fail {e}")
            raise e

    def get_by_weight(self, weight:float = 0) -> ModelWeightDelivery:
        try:
            weight_delivery = self.db_session.query(ModelWeightDelivery).filter(ModelWeightDelivery.delivery_threshold_pound <= weight).order_by(ModelWeightDelivery.delivery_threshold_pound.desc()).first()   
            return weight_delivery
        except Exception as e:
            self.log.error(f"file: weight_delivery_object.py method: get_by_weight fail {e}")
            raise e

    def delete_all(self, auto_commit: bool = True) -> None:
        return super().delete_all(auto_commit)
    
