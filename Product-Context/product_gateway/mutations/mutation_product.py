import time
import logging
import graphene
from graphql_relay import from_global_id
from product_ctx_database_sqlalchemy_14.models.product_model import (
    ModelProduct,
)
from product_ctx_database_sqlalchemy_14.objects.product_object import (
    ProductAttributesGateway,
    ProductDatabase,
)
from product_ctx_database_sqlalchemy_14.objects.media_object import (
    MediaAttributesGateway,
    MediaDataBase,
)
from nodes.product_media import Product


class ProductGraphAttribute:
    upc_barcode = graphene.String(
        description="UpcBarcode of the Product.", required=True
    )
    sub_category_id = graphene.ID(description="Id of the SubCategory", required=True)
    title = graphene.String(description="Title of the Product", required=True)
    size = graphene.String(description="Size of the Product", required=True)
    brand = graphene.String(description="Brand of the Product", required=True)
    retailer = graphene.String(description="Retailer of the Product", required=True)
    description = graphene.String(
        description="Description of the Product", required=True
    )
    cost = graphene.Float(description="Cost of the Product", required=True)


class UpdateProductGraphAttribute:
    id = graphene.ID(description="Id of the Product.", required=True)
    sub_category_id = graphene.ID(description="Id of the SubCategory", required=True)
    title = graphene.String(description="Title of the Product", required=True)
    size = graphene.String(description="Size of the Product", required=True)
    brand = graphene.String(description="Brand of the Product", required=True)
    retailer = graphene.String(description="Retailer of the Product", required=True)
    description = graphene.String(
        description="Description of the Product", required=True
    )
    cost = graphene.Float(description="Cost of the Product", required=True)


class MediaGraphAttribute:
    link_url = graphene.String(description="Image Url of the Product", required=True)
    is_main = graphene.Boolean(
        description="Is Main Image of the Product",
        default_value=False,
    )
    media_type = graphene.String(description="Media Type of the Product", required=True)
    name = graphene.String(description="Name of the Product", required=False)


class ProductGraphInput(graphene.InputObjectType, ProductGraphAttribute):
    """Arguments to create a Product."""


class UpdateProductGraphInput(graphene.InputObjectType, UpdateProductGraphAttribute):
    """Arguments to create a Product."""


class MediaGraphInput(graphene.InputObjectType, MediaGraphAttribute):
    """Arguments to create a Media."""


class CreateProduct(graphene.Mutation):
    """Create a Product."""

    product = graphene.Field(
        lambda: Product, description="Product created by this mutation."
    )

    class Arguments:
        product_input = ProductGraphInput(required=True)
        media_input = graphene.List(graphene.NonNull(MediaGraphInput), required=True)

    def mutate(self, info, product_input, media_input):
        log = logging.getLogger(__name__)
        log.info(f"CreateProduct Mutation: {product_input.get('upc_barcode')}")
        try:
            product_attributes = ProductAttributesGateway().from_dict(product_input)
        except Exception as e:
            raise Exception(f"Error in ProductGraphInput: {e}")
        # Instantiate the database object product and media

        product_db: ProductDatabase = ProductDatabase(log)
        media_db: MediaDataBase = MediaDataBase(log)

        # Get the id of the subcategory
        id_subcategory = int(from_global_id(product_attributes.sub_category_id).id)
        product_attributes.sub_category_id = id_subcategory
        # Create the product and media
        product_attributes.api_id = f"manual_created-{product_attributes.upc_barcode}"

        try:
            product_model = product_db.create(
                product=product_attributes,
                raise_integrety_except=True,
                auto_commit=False,
            )

            product_db.db_session.refresh(product_model)

        except Exception as e:
            product_db.db_session.rollback()
            if e.__class__.__name__ == "IntegrityError":
                if e.orig.pgerror.find("Product_api_id_key") != -1:
                    raise Exception(
                        f"Product already exists, upc_barcode: {product_attributes.upc_barcode}, error_code: $RPBUNIDB001"
                    )
                else:
                    raise Exception(
                        f"Error in CreateProduct: IntegrityError {e}, error_code: $RPBUNIDB002"
                    )
            else:
                raise Exception(
                    f"Error in CreateProduct: {e}, error_code: $RPBUNIDB003"
                )

        if product_model.id:
            try:
                for media in media_input:
                    media_attributes = MediaAttributesGateway().from_dict(media)
                    media_attributes.product_id = product_model.id
                    media_db.create(
                        media=media_attributes,
                    )
            except Exception as e:
                media_db.db_session.rollback()
                raise Exception(f"Error in MediaGraphInput: {e}")
        else:
            raise Exception(f"Error in CreateProduct")

        return CreateProduct(product=product_model)


class UpdateProduct(graphene.Mutation):
    """Update a Product."""

    product = graphene.Field(
        lambda: Product, description="Product updated by this mutation."
    )

    class Arguments:
        product_input = UpdateProductGraphInput(required=True)
        media_input = graphene.List(graphene.NonNull(MediaGraphInput), required=True)

    def mutate(self, info, product_input, media_input):
        log = logging.getLogger(__name__)
        log.info("UpdateProduct Mutation: %s", product_input.get("id"))

        product_db: ProductDatabase = ProductDatabase(log)
        media_db: MediaDataBase = MediaDataBase(log)

        product_id = int(from_global_id(product_input.id).id)
        old_product: ModelProduct = product_db.get(id=product_id)
        sub_category_id = int(from_global_id(product_input.sub_category_id).id)
        old_product.sub_category_id = sub_category_id
        old_product.name = product_input.title
        old_product.title = product_input.title
        old_product.size = product_input.size
        old_product.brand = product_input.brand
        old_product.retailer = product_input.retailer
        old_product.description = product_input.description
        old_product.cost = product_input.cost
        old_product.edited = int(time.time())
        try:
            new_product = product_db.update(
                product_model=old_product,
                raise_integrety_except=True,
                auto_commit=False,
            )

            try:
                media_db.delete_by_product_id(
                    product_id=old_product.id,
                    auto_commit=False,
                )
                for media in media_input:
                    media_attributes = MediaAttributesGateway().from_dict(media)
                    media_attributes.product_id = old_product.id
                    media_db.create(
                        media=media_attributes,
                    )
            except Exception as e:
                media_db.db_session.rollback()
                raise Exception(f"Error in UpdateMedia: {e}")
        except Exception as e:
            raise Exception(f"Error in UpdateProduct: {e}") from e
        return UpdateProduct(product=new_product)
