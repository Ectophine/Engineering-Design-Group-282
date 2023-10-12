from ED_app.cost import liters_conversion, temperature_conversion, c02_conversion
import random


def random_statement(df, water_use, gas_use):
    statement_number = random.randint(1, 2)
    if statement_number == 1:
        pools = liters_conversion(water_use, 'pools_kids')
        statement = 'You have saved enough liters of water to fill ' + str(pools) + ' kids swimming pools!'
    elif statement_number == 2:
        trees = liters_conversion(water_use, 'trees')
        statement = 'You have saved enough liters of water to water ' + str(trees) + ' trees!'

    return statement
