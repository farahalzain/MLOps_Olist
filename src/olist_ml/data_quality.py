import great_expectations as gx
from great_expectations import expectations as gxe


def validate_data_quality(df):
    """Validate input data quality using Great Expectations."""

    context = gx.get_context(mode="ephemeral")

    data_source = context.data_sources.add_pandas("olist_pandas")

    data_asset = data_source.add_dataframe_asset(name="olist_orders")

    batch_definition = data_asset.add_batch_definition_whole_dataframe("olist_orders_batch")

    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    expectations = [
    gxe.ExpectColumnValuesToNotBeNull(column="customer_state"),

    gxe.ExpectColumnValuesToBeBetween(column="total_price", min_value=0),

    gxe.ExpectColumnValuesToBeBetween(column="total_freight", min_value=0),

    gxe.ExpectColumnValuesToBeBetween(column="item_count", min_value=1),

    gxe.ExpectColumnValuesToBeBetween(column="distance_km", min_value=0),

    gxe.ExpectColumnValuesToBeInSet(column="customer_state",
    value_set=[
        "AC", "AL", "AP", "AM", "BA", "CE", "DF",
        "ES", "GO", "MA", "MT", "MS", "MG", "PA",
        "PB", "PR", "PE", "PI", "RJ", "RN", "RS",
        "RO", "RR", "SC", "SP", "SE", "TO",], ),
    ]

    gxe.ExpectColumnValuesToNotBeNull(column="total_price", mostly=0.99,),

    gxe.ExpectColumnValuesToBeInTypeList(column="total_price", type_list=["float64", "int64"],),

    gxe.ExpectColumnValuesToBeInTypeList(column="item_count", type_list=["int64"],),

    gxe.ExpectColumnValuesToBeInTypeList(column="customer_state", type_list=["object", "str"],),

    results = []

    for expectation in expectations:
        result = batch.validate(expectation)
        results.append(result)

    failed_expectations = [result
        for result in results
        if not result.success
    ]

    if failed_expectations:
        raise ValueError(
            f"Data quality validation failed: "
            f"{len(failed_expectations)} expectation(s) failed."
        )

    return True