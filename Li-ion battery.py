# LITHIUM-ION BATTERY PARAMETERS
volumetric_energy_density = 325  # Wh/L
gravimetric_energy_density = 150  # Wh/kg
charge_efficiency = 0.93         # Charging efficiency
discharge_efficiency = 0.94      # Discharging efficiency
round_trip_efficiency = charge_efficiency * discharge_efficiency  # Overall round-trip efficiency

# SYSTEM PARAMETERS
energy_consumption_TJ = 110161  # Energy consumption in TeraJoules over a year
storage_duration = 3            # Storage period in days
building_height = 8             # Height of the building (in meters)

# CONSTANTS
tera_to_kilo = 1_000_000_000    # Conversion from TJ to kWh (1 TJ = 1e9 kWh)
hours_in_a_day = 24             # Hours in a day
seconds_in_an_hour = 3600       # Seconds in one hour

# STEP 1: ENERGY CONSUMPTION CALCULATION
# Convert energy consumption from TeraJoules to Watt-hours (Wh) for the storage period
energy_consumption_Wh = (energy_consumption_TJ * tera_to_kilo * 1_000) / seconds_in_an_hour  # Convert TJ to Wh
storage_energy_Wh = (energy_consumption_Wh / 365) * storage_duration / 2  # Energy stored for 3 days (half charge-discharge cycle)

# STEP 2: ADJUST STORAGE CAPACITY FOR EFFICIENCIES
# Account for round-trip efficiency (charge and discharge losses)
storage_capacity_Wh = storage_energy_Wh / discharge_efficiency  # Required storage capacity in Wh considering efficiency

# STEP 3: BATTERY MASS AND VOLUME CALCULATIONS
battery_mass = storage_capacity_Wh / gravimetric_energy_density  # Mass of the battery in kg
battery_volume = storage_capacity_Wh / volumetric_energy_density  # Volume of the battery in liters
battery_volume_m3 = battery_volume / 1000                        # Convert volume from liters to cubic meters

# STEP 4: FOOTPRINT CALCULATION
battery_footprint = battery_volume_m3 / building_height  # Calculate footprint based on building height

# OUTPUT
print(f"Li-ion Battery Round-Trip Efficiency: {round_trip_efficiency:.4f}")
print(f"Energy Consumption for {storage_duration} days (in Wh): {storage_energy_Wh:.2f}")
print(f"Required Storage Capacity (in Wh): {storage_capacity_Wh:.2f}")
print(f"Li-ion Battery Mass (in kg): {battery_mass:.2f}")
print(f"Li-ion Battery Volume (in m³): {battery_volume_m3:.2f}")
print(f"Li-ion Battery Footprint (in m²): {battery_footprint:.2f}")

# ENERGY LOST DURING A CYCLE
charging_loss = storage_capacity_Wh * (1 - charge_efficiency)
discharging_loss = storage_capacity_Wh * (1 - discharge_efficiency)
energy_lost_Wh = charging_loss + discharging_loss
# energy_lost_Wh = storage_capacity_Wh * (1 - round_trip_efficiency)

# CONVERT TO kWh
energy_lost_kWh = energy_lost_Wh / 1000  # Convert Wh to kWh

# OUTPUT
print(f"Energy Lost During Charging (in kWh): {charging_loss/1000:.2f}")
print(f"Energy Lost During Discharging (in kWh): {discharging_loss/1000:.2f}")
print(f"Energy Lost During a Cycle (in kWh): {energy_lost_kWh:.2f}")

# SYSTEM PARAMETERS FOR WATER FLOW
initial_temperature = 20  # Initial temperature of water (in °C)
final_temperature = 25     # Final temperature of water (in °C)
delta_T = final_temperature - initial_temperature  # Temperature change (in °C)
specific_heat_capacity = 4186  # Specific heat capacity of water (in J/kg·°C)

# HEAT TRANSFER RATE (example value)
heat_transfer_rate = discharging_loss / (storage_duration * 24)  # Heat transfer rate (in Watts)

# CALCULATE MASS FLOW RATE (kg/s)
mass_flow_rate = heat_transfer_rate / (specific_heat_capacity * delta_T)

# OUTPUT RESULTS
print(f"Required Mass Flow Rate (in kg/s): {mass_flow_rate:.4f}")