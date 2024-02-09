if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    # Remove rows where the passenger count is equal to 0 and the trip distance is equal to zero.
    data = data[data['passenger_count'] > 0]
    data = data[data['trip_distance'] > 0]

    # Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    # Rename columns in Camel Case to Snake Case, e.g. VendorID to vendor_id
    data.columns = data.columns.str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True).str.lower()

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """

    assert output is not None, 'The output is undefined'

    # Add three assertions:
    #    vendor_id is one of the existing values in the column (currently)
    for _, value in output['vendor_id'].items():
        assert value >= 1
    #    passenger_count is greater than 0
    for _, value in output['passenger_count'].items():
        assert value > 0
    #    trip_distance is greater than 0
    for _, value in output['trip_distance'].items():
        assert value > 0

