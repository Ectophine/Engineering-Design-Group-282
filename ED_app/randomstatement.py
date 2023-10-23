from ED_app.cost import liters_conversion, temperature_conversion, c02_conversion
import random


def random_statement(df, water_use, gas_use):
    statement_number = random.randint(1, 8)
    if statement_number == 1:
        pools = liters_conversion(water_use, 'pools_kids')
        statement = 'You have saved enough liters of water to fill ' + str(round(pools, 2)) + ' kids swimming pools!'
    elif statement_number == 2:
        trees = liters_conversion(water_use, 'trees')
        statement = 'You have saved enough liters of water to water ' + str(round(trees, 2)) + ' trees!'
    elif statement_number == 3:
        beer_crates = liters_conversion(water_use, 'beer_crate')
        statement = 'The amount of water you have saved so far is the equivalent of ' + str(round(beer_crates, 2)) + ' meters of stacked beer crates!'
    elif statement_number == 4:
        water_bottles = liters_conversion(water_use, 'water_bottle')
        statement = 'The amount of water you have saved so far is the equivalent of ' + str(round(water_bottles, 2)) + ' meters of water bottles!'
    elif statement_number == 5:
        elephant_trunk = liters_conversion(water_use, 'elephant_trunk')
        statement = 'The amount of water you have saved so far is as much water as ' + str(round(elephant_trunk, 2)) + ' elephants can hold in their trunks!'
    elif statement_number == 6:
        fish_bowls = liters_conversion(water_use, 'fishbowl')
        statement = 'The amount of water you have saved so far could fill ' + str(round(fish_bowls, 2)) + ' average fish bowls!'
    elif statement_number == 7:
        families = liters_conversion(water_use, 'families')
        statement = 'The amount of water you have saved so far is the equivalent to the daily water usage of ' + str(round(families, 2)) + ' African families!'
    elif statement_number == 8:
        c02_used = liters_conversion(water_use, 'C02')
        car_km = c02_conversion(c02_used, 'car_km')
        statement = 'The amount of water you have saved so far saved ' + str(round(c02_used, 2)) + ' grams of c02! This equivalent to a car driving ' + str(round(car_km, 2)) + ' km!'

    return statement
