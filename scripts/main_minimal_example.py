# This code needs to be moved to the Global_Port_Optimisation directory to run

"""This is the main code for the global optimisation of the port network
This code just iterates over the scenarios and cases of interest.
The work is done by p_driver, which creates an instance of the optimisation model (defined in optimisation_parent),
and then solves it.
The purpose of the model is to optimise the distribution of ammonia given specific inputs relating to the supply chain.
N Salmon 7/12/2022"""

import p_optimisation_parent as optimisation_class
import xarray as xr
import pandas as pd
import p_toolbox as toolbox
import p_driver as dr
import p_select_locations as sl
import p_get_onshore_distances as od


def main(scenario, demand_data, case):
    print('Importing the data...')

    # Create optimisation class
    optimiser = optimisation_class.Optimiser()

    # Load in the base case information
    supplier_number = 20
    supplier_data = pd.read_csv(r'Ammonia Cost Data/c_{a}.csv'.format(a=scenario))  # Ammonia production
    supplier_data = sl.select_locations(supplier_data, number_of_locations=supplier_number, min_production=1)
    if len(supplier_data) < supplier_number:
        print('There are only {a} suppliers that meet that production requirement'.format(a=len(supplier_data)))

    # Keep a separate data frame with the needed info for saving outputs later
    location_elec_cost_frac = supplier_data.drop(columns=supplier_data.columns[1:-1]).set_index('Index')

    # Get the port data
    port_data = pd.read_csv(r'Ammonia Cost Data//c_port_data.csv')  # list of all ports

    # Get the onshore distance data
    onshore_distance_data = xr.open_dataset(r'Ammonia Cost Data//n_onshore_distances_{a}.nc'.format(a=scenario))
    # Checks if the onshore distance data is right for this dataset. If not, produces a new one.
    # if sorted(onshore_distance_data.ports.values.tolist()) != sorted(port_data.name.tolist()) or \
    #         sorted(onshore_distance_data.suppliers.values.tolist()) != sorted(supplier_data.Index.tolist()):
    #     print('The onshore distance dataset has changed. Fetching the new dataset...')
    # onshore_distance_data = od.get_onshore_distances(supplier_data, port_data.rename(columns={'name': 'port_name'}),
    #                                                  '4.5_cross_border_pipelines')

    # Load in cost data for both the small ship and the big ship...
    # Note: Using multiple ship sizes slows down the code a lot! The small ship size has been switched off.
    # (Switch off is done in fix_variables subroutine in p_toolbox)
    offshore_cost_data_s = xr.open_dataset(r'Ammonia Cost Data//return_costs_{a}_Large Handysize.nc'.format(a=scenario))
    offshore_cost_data_b = xr.open_dataset(r'Ammonia Cost Data//return_costs_{a}_Panamax.nc'.format(a=scenario))

    # Set up demand factor cases
    demand_factors = [1]

    # Get the demand information for case 1
    # limit_sites is just for debugging so you can speed up the code.
    # 'factor' is used to correct the data by any desirable property. Usually used to convert HFO to Ammonia.
    demand_df = toolbox.extract_demand_data(demand_data, scenario, case, factor=demand_factors[0])
    print(demand_df)
    demand_df = demand_df.head(5)

    # Create an initial instance of the class...
    instance = optimiser.create_instance(supplier_data, port_data, onshore_distance_data,
                                         offshore_cost_data_s, offshore_cost_data_b, demand_df)

    # Free up some memory...
    onshore_distance_data.close()
    offshore_cost_data_s.close()
    offshore_cost_data_b.close()

    # Simplify the instance to reduce the number of variables
    instance = toolbox.fix_variables(instance)

    for count, demand_factor in enumerate(demand_factors):
        file_name = '{a}_factor_{b}_reduced'.format(a=scenario, b=demand_factor)
        if count == 0:
            dr.driver(optimiser, instance, demand_data, scenario, case, file_name, location_elec_cost_frac)
        else:
            dr.driver(optimiser, instance, demand_data, scenario, case, file_name, location_elec_cost_frac,
                      reset_demand=True, overwrite_lb=True, demand_factor=demand_factor)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    demand_data = 'Port_fuel_demand/fuel_demand_port_2050_1000km.csv'
    case = 'Fuel_tons_route_future'
    main('4.5', demand_data, case)
