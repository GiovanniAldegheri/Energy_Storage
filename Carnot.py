# SYSTEM PARAMETERS
cold_side = 20          # Cold-side temperature (in Celsius)
hot_side = 650          # Hot-side temperature (in Celsius)
eff_heating = 0.98      # Efficiency of the heating coils
eff_secondary = 0.65    # Efficiency of the secondary system (e.g., power cycle)
eff_storage = 0.99      # Efficiency of the storage system
storage_duration = 3    # Duration of energy storage (in days)
height = 24             # Height of the storage facility (in meters)
energy_consumption_TJ = 110161  # Energy consumption in TeraJoules per year

# DIABASE PROPERTIES (storage material)
density = 3007                 # Density of diabase (in kg/m³)
heat_capacity = 3824.9         # Heat capacity of diabase (in kJ/K/m³)

# CONSTANTS
tera_to_kilo = 1_000_000_000   # Conversion factor from Tera to kilo
seconds_in_an_hour = 3600      # Seconds in an hour

# STEP 1: CARNOT EFFICIENCY CALCULATION
# Carnot efficiency based on the cold-side and hot-side temperatures (converted to Kelvin)
eff_carnot = 1 - ((cold_side + 273) / (hot_side + 273))

# STEP 2: FINAL SYSTEM EFFICIENCY
# Final system efficiency considering the secondary system and Carnot efficiency
eff_final = eff_secondary * eff_carnot
eff_rt = eff_final*eff_heating*(eff_storage)**storage_duration

# OUTPUT CARNOT AND FINAL EFFICIENCIES
print(f"Carnot Efficiency: {eff_carnot:.4f}")
print(f"Final System Efficiency: {eff_final:.4f}")
print(f"Round Trip Efficiency: {eff_rt:.4f}")

# STEP 3: ENERGY CONSUMPTION CALCULATION
# Convert energy consumption from TeraJoules to Watt-hours (Wh) for the storage period
energy_consumption_Wh = (energy_consumption_TJ * tera_to_kilo * 1_000) / seconds_in_an_hour  # Convert TJ to Wh
storage_energy_Wh = (energy_consumption_Wh / 365) * storage_duration / 2  # Energy stored for 3 days (half charge-discharge cycle)

# STEP 4: STORAGE CAPACITY CALCULATION (Excluding heating efficiency)
# Calculating the required storage capacity, considering only final system efficiency and storage efficiency
storage_capacity_Wh = storage_energy_Wh / (eff_final * (eff_storage ** storage_duration))

# STEP 5: STORAGE VOLUME CALCULATION
# Calculating the required volume of the storage material based on heat capacity and temperature difference
heat_capacity_wh = heat_capacity * 0.27778
storage_volume_m3 = storage_capacity_Wh / (heat_capacity_wh * (hot_side - cold_side))  # Volume in cubic meters

# STEP 6: STORAGE MASS CALCULATION
# Total mass of storage material needed based on volume and density
storage_mass = storage_volume_m3 * density  # Mass in kg

# STEP 7: FOOTPRINT CALCULATION
# Horizontal footprint of the storage facility based on its height
footprint = storage_volume_m3 / height  # Footprint in square meters

# OUTPUT RESULTS
print(f"Energy Consumption for {storage_duration} days (in Wh): {storage_energy_Wh:.2f}")
print(f"Required Storage Capacity (in Wh): {storage_capacity_Wh:.2f}")
print(f"Required Storage Volume (in m³): {storage_volume_m3:.2f}")
print(f"Total Storage Mass (in kg): {storage_mass:.2f}")
print(f"Storage Footprint (in m²): {footprint:.2f}")

# ENERGY LOST DURING A CYCLE
charging_loss_Wh = storage_capacity_Wh * (1 - eff_heating)
discharging_loss_Wh = storage_capacity_Wh - storage_energy_Wh
energy_lost_Wh = charging_loss_Wh + discharging_loss_Wh

# CONVERT TO kWh
energy_lost_kWh = energy_lost_Wh / 1000  # Convert Wh to kWh

# OUTPUT
print(f"Energy Lost During Charging (in kWh): {charging_loss_Wh/1000:.2f}")
print(f"Energy Lost During Discharging (in kWh): {discharging_loss_Wh/1000:.2f}")
print(f"Energy Lost During a Cycle (in kWh): {energy_lost_kWh:.2f}")

# SYSTEM PARAMETERS FOR WATER FLOW
initial_temperature = 20  # Initial temperature of water (in °C)
final_temperature = 25   # Final temperature of water (in °C)
delta_T = final_temperature - initial_temperature  # Temperature change (in °C)
specific_heat_capacity = 4186  # Specific heat capacity of water (in J/kg·°C)

# HEAT TRANSFER RATE (example value)
heat_transfer_rate = discharging_loss_Wh / (storage_duration * 24)  # Heat transfer rate (in Watts)

# CALCULATE MASS FLOW RATE (kg/s)
mass_flow_rate = heat_transfer_rate / (specific_heat_capacity * delta_T)

# OUTPUT RESULTS
print(f"Required Mass Flow Rate (in kg/s): {mass_flow_rate:.4f}")

