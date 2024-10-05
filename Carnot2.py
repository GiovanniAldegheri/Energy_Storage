# SYSTEM PARAMETERS
hot_side = 650          # Hot-side temperature (in Celsius)
eff_heating = 0.98      # Efficiency of the heating coils
eff_secondary = 0.65    # Efficiency of the secondary system (e.g., power cycle)
eff_storage = 0.99      # Efficiency of the storage system
storage_duration = 3    # Duration of energy storage (in days)
height = 24             # Height of the storage facility (in meters)
energy_consumption_TJ = 110161  # Energy consumption in TeraJoules per year

# DIABASE PROPERTIES (storage material)
density = 3007                 # Density of diabase (in kg/m³)
heat_capacity_kJ = 3824.9         # Heat capacity of diabase (in kJ/K/m³)

# CONSTANTS
seconds_in_an_hour = 3600      # Seconds in an hour

def calculate_efficiencies(cold_side):
    # STEP 1: CARNOT EFFICIENCY CALCULATION
    eff_carnot = 1 - ((cold_side + 273) / (hot_side + 273))

    # STEP 2: FINAL SYSTEM EFFICIENCY
    eff_final = eff_secondary * eff_carnot
    eff_rt = eff_final * eff_heating * (eff_storage ** storage_duration)

    return eff_carnot, eff_final, eff_rt

def calculate_storage_energy():
    # STEP 3: ENERGY CONSUMPTION CALCULATION
    energy_consumption_Wh = (energy_consumption_TJ * 1_000_000_000_000) / seconds_in_an_hour  # Convert TJ to Wh
    storage_energy_Wh = (energy_consumption_Wh / 2 / 365) * storage_duration  # Energy stored for 3 days (half of denmark)
    
    return storage_energy_Wh

def calculate_storage_capacity(storage_energy_Wh, eff_final):
    # STEP 4: STORAGE CAPACITY CALCULATION (Excluding heating efficiency)
    storage_capacity_Wh = storage_energy_Wh / (eff_final * (eff_storage ** storage_duration))
    
    return storage_capacity_Wh

def calculate_storage_volume(storage_capacity_Wh):
    # STEP 5: STORAGE VOLUME CALCULATION
    heat_capacity_wh = heat_capacity_kJ * 0.27778 #Convert kJ to Wh
    storage_volume_m3 = storage_capacity_Wh / (heat_capacity_wh * (hot_side - cold_side))  # Volume in cubic meters
    
    return storage_volume_m3

def calculate_storage_mass(storage_volume_m3):
    # STEP 6: STORAGE MASS CALCULATION
    storage_mass = storage_volume_m3 * density  # Mass in kg
    
    return storage_mass

def calculate_footprint(storage_volume_m3):
    # STEP 7: FOOTPRINT CALCULATION
    footprint = storage_volume_m3 / height  # Footprint in square meters
    
    return footprint

def calculate_energy_losses(storage_capacity_Wh, storage_energy_Wh):
    # ENERGY LOST DURING A CYCLE
    charging_loss_Wh = storage_capacity_Wh * (1 - eff_heating)
    discharging_loss_Wh = storage_capacity_Wh - storage_energy_Wh
    energy_lost_Wh = charging_loss_Wh + discharging_loss_Wh

    # CONVERT TO kWh
    energy_lost_kWh = energy_lost_Wh / 1000  # Convert Wh to kWh

    return charging_loss_Wh, discharging_loss_Wh, energy_lost_kWh

def calculate_mass_flow_rate(discharging_loss_Wh, final_temperature):
    # SYSTEM PARAMETERS FOR WATER FLOW
    initial_temperature = 20  # Initial temperature of water (in °C)
    delta_T = final_temperature - initial_temperature  # Temperature change (in °C)
    if delta_T == 0:
        delta_T = 5
    specific_heat_capacity = 4186  # Specific heat capacity of water (in J/kg·°C)

    # HEAT TRANSFER RATE (example value)
    heat_transfer_rate = discharging_loss_Wh / (storage_duration * 24)  # Heat transfer rate (in Watts)

    # CALCULATE MASS FLOW RATE (kg/s)
    mass_flow_rate = heat_transfer_rate / (specific_heat_capacity * delta_T)

    if final_temperature == 70:
        q_heating = mass_flow_rate * specific_heat_capacity * 30 * storage_duration * 24
        print(f"Energy Used for Heating (in MWh): {q_heating/1_000_000:.2f}")
    
    return mass_flow_rate

def run_calculations(cold_side):
    eff_carnot, eff_final, eff_rt = calculate_efficiencies(cold_side)
    storage_energy_Wh = calculate_storage_energy()
    storage_capacity_Wh = calculate_storage_capacity(storage_energy_Wh, eff_final)
    storage_volume_m3 = calculate_storage_volume(storage_capacity_Wh)
    storage_mass = calculate_storage_mass(storage_volume_m3)
    footprint = calculate_footprint(storage_volume_m3)
    charging_loss_Wh, discharging_loss_Wh, energy_lost_kWh = calculate_energy_losses(storage_capacity_Wh, storage_energy_Wh)
    mass_flow_rate = calculate_mass_flow_rate(discharging_loss_Wh, cold_side)

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
    print(f"Required Mass Flow Rate (in kg/s): {mass_flow_rate:.4f}")

# Example of running calculations for different cold side temperatures
cold_side_temperatures = [20, 70]  # List of different cold side temperatures in Celsius
for cold_side in cold_side_temperatures:
    print(f"\nCalculations for Cold Side Temperature: {cold_side} °C")
    run_calculations(cold_side)