# Cost functions and constants

# Cost per liter, Dutch average
moneyLiter = 1000 / 1.03
# Liters in an Olympic swimming pool
poolsLiter_olympic = 2500000
# Liters in a child-sized pool
poolsLiter_kids = 400
#  Daily water usage of a tree
treesLiter = 1600
# Daily water usage of an African family, 5 gallons
Family_usage = (5 * 3.78541178)
# Grams of C02 per cleaned liter of water
C02_water = 0.3 * 10 ** -3
# Liters in an average elephant trunk
elephant_trunk = 16
# Liters in a fishbowl
fishbowl = 3
# 45 mL in an average water balloon
water_balloon = 45*10**-3
# Liters per meter height when stacking water bottles of 0.5L
water_bottle_height = 2.5
# Liters per meter height when stacking beer crates
beer_crate_height = 34.435
# Liters of blood in the average human
blood_volume = 5
# Liters of urine daily
urine_volume_daily = 1.4

# Heat capacity of one liter water, J/L?C
C = 4.2 * 10 ** 3
# Average temperature of water in pipes in summer, Celsius
T_pipes_summer = 17.5
# Average temperature of water in pipes in winter, Celsius
T_pipes_winter = 12.5
# Heat of combustion of natural gas
Rv = 31.65 * 10 ** 6
# Efficiency of a boiler
efficiency = 0.73
# Current gas price per m^3
gasprice = 1.314
# kg of C02 per burned cubic meter of natural gas
C02_gas = 1.9

# Amount of carbon from one kg of C02
Carbon = 0.27
# Amount of carbon in an average tree
Carbon_tree = 500
# kg of C02 a tree captures annually
C02_trees_yearly = 25
# Amount of C02 emissions per km driven by a car
Car_km = 95.1


def liter_per_t(liters, dt):
    return liters * dt


def liters_conversion(liters, metric='money'):
    if metric == 'money':
        conversion = liters / moneyLiter
    if metric == 'pools_olympic':
        conversion = liters / poolsLiter_olympic
    if metric == 'pools_kids':
        conversion = liters / poolsLiter_kids
    if metric == 'trees':
        conversion = liters / treesLiter
    if metric == 'families':
        conversion = liters / Family_usage
    if metric == 'C02':
        conversion = liters * C02_water
    if metric == 'elephant_trunk':
        conversion = liters/elephant_trunk
    if metric == 'fishbowl':
        conversion = liters/fishbowl
    if metric == 'water_balloon':
        conversion = liters/water_balloon
    if metric == 'water_bottle':
        conversion = liters/water_bottle_height
    if metric == 'beer_crate':
        conversion = liters/beer_crate_height
    if metric == 'blood':
        conversion = liters/blood_volume
    if metric == 'urine_days':
        conversion = liters/urine_volume_daily
    return conversion


def temperature_conversion(temperature, liters, metric, date):
    if 4 < 5 < 11:
        season = 'summer'
    else:
        season = 'winter'

    if season == 'summer':
        T_pipes = T_pipes_summer
    if season == 'winter':
        T_pipes = T_pipes_winter

    gas = C * (temperature - T_pipes) / (Rv * efficiency) * liters

    if metric == 'gas':
        return gas
    if metric == 'money':
        conversion = gas * gasprice  # + liters_conversion(liters, 'money')
    if metric == 'C02':
        conversion = gas * C02_gas  # + liters_conversion(liters, 'C02')
    return conversion


def c02_conversion(c02, metric='carbon'):
    if metric == 'carbon':
        conversion = c02 * Carbon
    if metric == 'trees':
        conversion = c02 * Carbon / Carbon_tree
    if metric == 'trees_yearly':
        conversion = c02 / C02_trees_yearly
    if metric == 'car_km':
        conversion = c02 / Car_km
    return conversion
