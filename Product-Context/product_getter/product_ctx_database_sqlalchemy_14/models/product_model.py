from typing import Any, Dict
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Index,Computed,Enum, Boolean
from sqlalchemy.orm import relationship
from product_ctx_database_sqlalchemy_14.models.base import Base
from product_ctx_database_sqlalchemy_14.models.category_model import ModelCategory
from product_ctx_database_sqlalchemy_14.models.media_model import ModelMedia
from product_ctx_database_sqlalchemy_14.models.product_retailer_model import ModelProductRetailer
from sqlalchemy_utils.types.ts_vector import TSVectorType


class ModelProduct(Base):
    """Product model."""    
    
    __tablename__ = "Product"
    
    weight_enum = Enum("ounce", "pound", "kilo", "gram","liter","gallon","milliliter" ,name="weight")


    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, doc="Id of the Product")
    sub_category_id = Column(ForeignKey('SubCategory.id', ondelete='CASCADE'), doc="Foreign ID Id of the SubCategory", primary_key=True)
    api_id = Column(String(300), unique=True, nullable=False, doc="ApiID of the Product")
    name = Column(String(200), unique=False, doc="Name of the Product and unique")
    title = Column(String(250), unique=False, doc="Title of the Product")
    words_tags = Column(String(250), nullable=False, doc="TagsWords of the Product")
    brand = Column(String(100), nullable=True, doc="Brand of the Product")
    base_increment = Column(Float, doc="Increment of the Product", default=None)
    description = Column(String(2500), nullable=False, doc="Description of the Product")
    upc_barcode = Column( String(100), nullable=True, unique=True, doc="UpcBarcode of the Product.")
    unit_measure = Column(weight_enum, nullable=True, doc="UnitMeasure of the Product.")
    weight = Column(Float, nullable=True, doc="Weight of the Product.")
    size = Column(String,  nullable=True, doc="Size of the Product.Example 20x20x20 in cm")
    unit_in_pack = Column(Integer, nullable=True, doc="Unit in Pack of the Product")
    dpci = Column(String(30),  nullable=True, doc="Stands for Department, Class, Item. (DPCI) is a unique identifier assigned to each product in Target's inventory.")
    tcin = Column(Integer,  nullable=True, doc="Stands for Target Corporation Identification Number.(TCIN) It's similar in function to DPCI but might represent a broader range of products or be used in a different context.")
    is_active = Column(Boolean, doc="Status of the Product",  default=True)
    created = Column(Integer, nullable=False, doc="Unix Timestamp when is the product created")
    edited = Column(Integer, nullable=True, doc="Unix Timestamp when is the product edited")
    
   
    words_tags_tsv = Column(
        TSVectorType("words_tags", regconfig="english"),
        Computed("to_tsvector('english', \"words_tags\")", persisted=True))
    
    
    title_tsv = Column(
        TSVectorType("title", regconfig="english"),
        Computed("to_tsvector('english', \"title\")", persisted=True))
    
    
    brand_tsv = Column(
        TSVectorType("brand", regconfig="english"),
        Computed("to_tsvector('english', \"brand\")", persisted=True))
    
    
    __table_args__ = (
        # Indexing the TSVector column
        Index("idx_Product_title_tsv", title_tsv, postgresql_using="gin"), 
        Index("idx_Product_brand_tsv", brand_tsv, postgresql_using="gin"),
        Index("idx_Product_words_tags_tvs", words_tags_tsv, postgresql_using="gin"))
    
    media_edge = relationship(
        ModelMedia,
        passive_deletes=True,
        cascade="all, delete-orphan",
        backref="Product",
        lazy='selectin')
    
    retailer_edge = relationship(
        ModelProductRetailer,
        passive_deletes=True,
        cascade="all, delete-orphan",
        backref="Product",
        lazy="selectin"
        )
    
    
    
    def to_dict(self) -> Dict[str, Any]:

        """return  shallow copy ModelProduct to dict """
        obj_dict = self.__dict__.copy()
        return {
            key: obj_dict.get(key)
            for key in obj_dict
            if key in ModelProduct.__dict__.keys()
        }

