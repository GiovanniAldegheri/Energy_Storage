# LITHIUM-ION BATTERY PARAMETERS
volumetric_energy_density = 325   # Wh/L
gravimetric_energy_density = 150  # Wh/kg
charge_efficiency = 0.93          # Charging efficiency
discharge_efficiency = 0.94       # Discharging efficiency
round_trip_efficiency = charge_efficiency * discharge_efficiency  # Overall round-trip efficiency

# SYSTEM PARAMETERS
energy_consumption_TJ = 110161    # Energy consumption in TeraJoules over a year
storage_duration = 3              # Storage period in days
building_height = 8               # Height of the building (in meters)

# CONSTANTS
tera_to_kilo = 1_000_000_000      # Conversion from TJ to kWh (1 TJ = 1e9 kWh)
hours_in_a_day = 24               # Hours in a day
seconds_in_an_hour = 3600         # Seconds in one hour

# CALCULATIONS

# STEP 1: ENERGY CONSUMPTION CALCULATION
energy_consumption_Wh = (energy_consumption_TJ * tera_to_kilo * 1_000) / seconds_in_an_hour
storage_energy_Wh = (energy_consumption_Wh / 365) * storage_duration / 2  # Half charge-discharge cycle

# STEP 2: ADJUST STORAGE CAPACITY FOR EFFICIENCIES
storage_capacity_Wh = storage_energy_Wh / discharge_efficiency  # Considering efficiency losses

# STEP 3: BATTERY MASS AND VOLUME CALCULATIONS
battery_mass = storage_capacity_Wh / gravimetric_energy_density  # Mass in kg
battery_volume_m3 = (storage_capacity_Wh / volumetric_energy_density) / 1000  # Volume in m³

# STEP 4: FOOTPRINT CALCULATION
battery_footprint = battery_volume_m3 / building_height  # Footprint in m²

# OUTPUT RESULTS
print(f"Li-ion Battery Round-Trip Efficiency: {round_trip_efficiency:.4f}")
print(f"Energy Consumption for {storage_duration} days (in MWh): {storage_energy_Wh / 1_000_000:.2f}")
print(f"Required Storage Capacity (in MWh): {storage_capacity_Wh / 1_000_000:.2f}")
print(f"Li-ion Battery Mass (in kg): {battery_mass:.2f}")
print(f"Li-ion Battery Volume (in m³): {battery_volume_m3:.2f}")
print(f"Li-ion Battery Footprint (in m²): {battery_footprint:.2f}")

# STEP 5: ENERGY LOSS DURING A CYCLE
charging_loss_Wh = storage_capacity_Wh * (1 - charge_efficiency)
discharging_loss_Wh = storage_capacity_Wh * (1 - discharge_efficiency)
energy_lost_Wh = charging_loss_Wh + discharging_loss_Wh
# OUTPUT ENERGY LOSSES
print(f"Energy Lost During Charging (in kWh): {charging_loss_Wh / 1_000:.2f}")
print(f"Energy Lost During Discharging (in kWh): {discharging_loss_Wh / 1_000:.2f}")
print(f"Energy Lost During a Cycle (in kWh): {energy_lost_Wh / 1_000:.2f}")

# STEP 6: MASS FLOW RATE CALCULATION (for cooling system)
initial_temperature = 20  # Initial water temperature (°C)
final_temperature = 25    # Final water temperature (°C)
delta_T = final_temperature - initial_temperature  # Temperature difference (°C)
specific_heat_capacity = 4186  # Specific heat capacity of water (J/kg·°C)

# Heat transfer rate (W)
heat_transfer_rate = discharging_loss_Wh / (storage_duration * hours_in_a_day)  # W

print(f"Heat Transfer Rate (in kW): {heat_transfer_rate / 1_000:.4f}")

# Calculate mass flow rate (kg/s)
mass_flow_rate = heat_transfer_rate / (specific_heat_capacity * delta_T)

# OUTPUT MASS FLOW RATE
print(f"Required Mass Flow Rate (in kg/s): {mass_flow_rate:.4f}")
