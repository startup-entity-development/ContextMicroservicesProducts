from product_ctx_database_sqlalchemy_14.objects.product_object import UnitMeasure


if __name__ == "__main__":
    unit = UnitMeasure.get_unit_measure("goz")
    print(unit)