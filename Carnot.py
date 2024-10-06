# SYSTEM PARAMETERS 
max_temp = 700
min_temp = 350
working_temp = 650  # Hot-side temperature (in Celsius)
eff_heating = 0.98  # Efficiency of the heating coils
eff_secondary = 0.65  # Efficiency of the secondary system (e.g., power cycle)
eff_storage = 0.99  # Efficiency of the storage system
storage_duration = 3  # Duration of energy storage (in days)
height = 24  # Height of the storage facility (in meters)
energy_consumption_TJ = 110161  # Energy consumption in TeraJoules per year

# DIABASE PROPERTIES (storage material)
density = 3007  # Density of diabase (in kg/m³)
heat_capacity_kJ = 3824.9  # Heat capacity of diabase (in kJ/K/m³)

# CONSTANTS
seconds_in_an_hour = 3600  # Seconds in an hour

# EFFICIENCY AND STORAGE ENERGY CALCULATIONS
def run_calculations(cold_side):
    eff_carnot = 1 - ((cold_side + 273) / (working_temp + 273))
    eff_final = eff_secondary * eff_carnot
    eff_rt = eff_final * eff_heating * (eff_storage ** storage_duration)

    energy_consumption_Wh = (energy_consumption_TJ * 1_000_000_000_000) / seconds_in_an_hour  # TJ to Wh
    storage_energy_Wh = (energy_consumption_Wh / 2 / 365) * storage_duration  # Energy stored for 3 days
    
    storage_capacity_Wh = storage_energy_Wh / (eff_final * (eff_storage ** storage_duration))

    heat_capacity_wh = heat_capacity_kJ * 0.27778  # Convert kJ to Wh
    storage_volume_m3 = storage_capacity_Wh / (heat_capacity_wh * (max_temp - min_temp))  # Volume in m³
    storage_mass = storage_volume_m3 * density  # Mass in kg
    footprint = storage_volume_m3 / height  # Footprint in m²

    charging_loss_Wh = storage_capacity_Wh * (1 - eff_heating)
    discharging_loss_Wh = storage_capacity_Wh - storage_energy_Wh
    energy_lost_kWh = (charging_loss_Wh + discharging_loss_Wh) / 1000  # Convert Wh to kWh

    # Water mass flow rate for discharging losses
    delta_T = cold_side - 20  # Temperature difference (in °C)
    if delta_T == 0:
        delta_T = 5
    specific_heat_capacity = 4186  # Specific heat capacity of water (in J/kg·°C)
    heat_transfer_rate = discharging_loss_Wh / (storage_duration * 24)  # Heat transfer rate in W
    mass_flow_rate = heat_transfer_rate / (specific_heat_capacity * delta_T)


    # OUTPUT RESULTS
    print(f"Carnot Efficiency: {eff_carnot:.4f}")
    print(f"Final System Efficiency: {eff_final:.4f}")
    print(f"Round Trip Efficiency: {eff_rt:.4f}")
    print(f"Energy Consumption for {storage_duration} days (in MWh): {storage_energy_Wh/1_000_000:.2f}")
    print(f"Required Storage Capacity (in MWh): {storage_capacity_Wh/1_000_000:.2f}")
    print(f"Required Storage Volume (in m³): {storage_volume_m3:.2f}")
    print(f"Total Storage Mass (in kg): {storage_mass:.2f}")
    print(f"Storage Footprint (in m²): {footprint:.2f}")
    print(f"Energy Lost During Charging (in MWh): {charging_loss_Wh/1_000_000:.2f}")
    print(f"Energy Lost During Discharging (in kWh): {discharging_loss_Wh/1_000:.2f}")
    print(f"Energy Lost During a Cycle (in MWh): {energy_lost_kWh/1_000:.2f}")
    if cold_side == 70:
        q_heating = mass_flow_rate * specific_heat_capacity * 30 * storage_duration * 24
        print(f"Energy Used for Heating (in MWh): {q_heating/1_000_000:.2f}")
    print(f"Required Mass Flow Rate (in kg/s): {mass_flow_rate:.4f}")

# Run calculations for different cold-side temperatures
cold_side_temperatures = [20, 70]  # Cold side temperatures in Celsius
for cold_side in cold_side_temperatures:
    print(f"\nCalculations for Cold Side Temperature: {cold_side} °C")
    run_calculations(cold_side)
