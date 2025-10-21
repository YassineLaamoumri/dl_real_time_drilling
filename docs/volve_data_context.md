# Volve Dataset: Depth vs. Time Logs Context

## Overview
The Equinor Volve field dataset (publicly released WITSML data from the North Sea) organizes raw drilling telemetry into two main folders: `depth/` and `time/`. This split follows standard oil & gas industry practices for handling measured depth (MD)-based vs. elapsed time (ELT)-based logging. 

- **Source**: Derived from WITSML (Wellsite Information Transfer Standard Markup Language) exports, converted to CSV.
- **Purpose**: Separates geological/subsurface snapshots (depth-tied) from operational/rig performance data (time-series).
- **Key Files**: Each well (e.g., 15/9-F-9 A) has corresponding CSVs like `Norway-NA-15_$47$_9-F-9 A depth.csv` and `Norway-NA-15_$47$_9-F-9 A time.csv`.
- **Challenges**: Mixed data types (strings, numerics, timestamps); potential encoding issues; need for alignment (time-to-depth interpolation).

## Depth Logs (`depth/` folder)
These CSVs log data sampled at specific **measured depths** along the wellbore (in meters or TVD - True Vertical Depth). They provide a static view of the subsurface as the drill advances.

### Typical Columns & Meaning
Based on the header from `Norway-NA-15_$47$_9-F-9 A depth.csv`, columns are extensive (100+), covering multiple sensor streams. Grouped below with explanations derived from standard drilling/WITSML terminology:

- **Depth-related**:
  - `Measured Depth m`: Cumulative distance along the wellbore from surface (MD, in meters).
  - `Extrapolated Hole TVD m`: Estimated True Vertical Depth (TVD) at current MD.
  - `Total Vertical Depth m`: Overall TVD drilled so far.
  - `Hole Depth (TVD) m`: Current hole TVD.
  - `Hole depth (MD) m`: Current hole MD.
  - `Bit Depth m`: Depth of the drill bit.
  - `Lag Depth (TVD) m`: TVD where mud returns are sampled (accounts for lag time).

- **Drilling Dynamics**:
  - `Rate of Penetration m/h`: ROP (speed of bit advance, meters per hour).
  - `Rate of penetration m/h`: Duplicate/alternative ROP measure.
  - `Rate of Penetration (5ft avg) m/h`: Smoothed ROP over 5-foot interval.
  - `1/2ft ROP m/h`: High-resolution ROP over half-foot.
  - `Inverse ROP s/m`: Time per meter drilled (1/ROP).
  - `Inverse ROP (5ft avg) s/m`: Smoothed inverse ROP.
  - `ROPIH s/m`: Inverse ROP in seconds per meter (possibly interval-specific).
  - `Bit Drill Time h`: Cumulative hours bit has been drilling.
  - `Bit Drilling Time h`: Active drilling time for current bit run.
  - `Bit Drilling Run m`: Distance drilled in current bit run.
  - `Bit run number unitless`: Sequential number of bit changes.
  - `Total Bit Revolutions unitless`: Cumulative bit rotations.
  - `Bit Revolutions (cum) unitless`: Running total of bit revs.
  - `Average Rotary Speed rpm`: Mean RPM of rotary table/drill string.
  - `Averaged RPM rpm`: Smoothed RPM value.
  - `Total Downhole RPM rpm`: RPM at bit (MWD-measured).
  - `MWD Turbine RPM rpm`: RPM from downhole turbine sensor.
  - `MWD Collar RPM rpm`: RPM at MWD tool collar.
  - `MWD Stick-Slip PKtoPK RPM rpm`: Peak-to-peak RPM variation (stick-slip vibration indicator).
  - `Weight on Bit kkgf`: Force applied to bit (kilo-kilograms force).
  - `Averaged WOB kkgf`: Smoothed WOB.
  - `Corrected Surface Weight on Bit kkgf`: Adjusted surface WOB for buoyancy/friction.
  - `Corrected Hookload kkgf`: Adjusted hook load.
  - `Average Hookload kkgf`: Mean hook load.
  - `Total Hookload kkgf`: Total weight on hook.
  - `Corrected Total Hookload kkgf`: Adjusted total hook load.
  - `HKLO kkgf`: Hook load out (possibly off-bottom).
  - `HKLI kkgf`: Hook load in (possibly on-bottom).
  - `Weight On Hook kkgf`: Direct hook weight.
  - `"String weight (rot,avg) kkgf"`: Average rotating drill string weight.
  - `Averaged TRQ kN.m`: Smoothed torque.
  - `Average Surface Torque kN.m`: Mean torque at surface.
  - `Average Standpipe Pressure kPa`: Mean pressure in standpipe.
  - `Stand Pipe Pressure kPa`: Instantaneous standpipe pressure.

- **Geological/MWD (Measurement While Drilling)**:
  - `MWD Raw Gamma Ray 1/s`: Raw gamma ray counts (radioactivity for lithology).
  - `MWD Gamma Ray (API BH corrected) gAPI`: Corrected gamma in API units (bottom-hole).
  - `ARC Gamma Ray (BH corrected) gAPI`: Annular/ARC tool gamma ray.
  - `MWD Continuous Inclination dega`: Real-time inclination (well deviation, degrees).
  - `MWD Continuous Azimuth dega`: Real-time azimuth (direction, degrees).
  - `MWD Gravity Toolface dega`: Toolface relative to gravity.
  - `MWD Magnetic Toolface dega`: Toolface relative to magnetic north.
  - `MWD GR Bit Confidence Flag %`: Confidence in gamma ray at bit position.
  - `AVG_CONF unitless`: Average confidence (sensor/general).
  - `MIN_CONF unitless`: Minimum confidence.
  - `IMP/ARC Non-BHcorr Phase-Shift Resistivity 28-in. at 2 MHz ohm.m`: Resistivity (phase-shift, non-corrected, 28-inch tool).
  - `IMP/ARC Non-BHcorr Phase-Shift Resistivity 40-in. at 2 MHz ohm.m`: Similar for 40-inch.
  - `IMP/ARC Non-BHcorr Attenuation Resistivity 28-in. at 2 MHz ohm.m`: Attenuation-based resistivity.
  - `IMP/ARC Non-BHcorr Attenuation Resistivity 40-in. at 2 MHz ohm.m`: 40-inch version.
  - `IMP/ARC Attenuation Conductivity 40-in. at 2 MHz mS/m`: Conductivity from attenuation.
  - `IMP/ARC Phase-Shift Conductivity 28-in. at 2 MHz mS/m`: Phase-shift conductivity.
  - `IMP/ARC Phase-Shift Conductivity 40-in. at 2 MHz mS/m`: 40-inch version.
  - `MWD Shock Peak m/s2`: Peak downhole vibration/shock.
  - `PowerUP Shock Rate 1/s`: Shock event frequency.
  - `MWD Total Shocks unitless`: Cumulative shocks detected.
  - `MWD Shock Risk unitless`: Risk level from shocks.
  - `MWD DNI Temperature degC`: Downhole tool temperature.

- **Mud/Fluid**:
  - `Mud Density In g/cm3`: Mud weight entering hole.
  - `Mud Density In g/cm3.1`: Duplicate/alternative mud in density.
  - `Mud Density Out g/cm3`: Mud weight returning (indicates gains/losses).
  - `Mud Flow In L/min`: Flow rate in.
  - `Flow Pumps L/min`: Total pump flow.
  - `TMP In degC`: Temperature of mud pump in.
  - `Temperature Out degC`: Mud temperature returning.
  - `Annular Temperature degC`: Temperature in annulus.
  - `ARC Annular Pressure kPa`: Pressure in annulus.
  - `Tank volume (active) m3`: Active mud tank volume.
  - `IMWT g/cm3`: Inferred mud weight?
  - `S1AC kPa`, `S2AC kPa`: Sensor pressures (possibly annular or static).

- **Gas/Chromatography** (Mud Gas Logging):
  - `Methane (C1) ppm`: Methane concentration in mud returns.
  - `Ethane (C2) ppm`: Ethane.
  - `Propane (C3) ppm`: Propane.
  - `Iso-butane (IC4) ppm`: Iso-butane.
  - `Nor-butane (NC4) ppm`: Normal butane.
  - `Iso-pentane (IC5) ppm`: Iso-pentane.
  - `n-Penthane ppm`: Normal pentane.
  - `Gas (avg) %`: Average total gas content.

- **Pumps & Strokes**:
  - `Pump 1 Stroke Rate 1/min`: Strokes per minute for pump 1.
  - `Pump 2 Stroke Rate 1/min`: For pump 2.
  - `Pump 3 Stroke Rate 1/min`: Pump 3.
  - `Pump 4 Stroke Rate 1/min`: Pump 4.
  - `Total SPM 1/min`: Total strokes per minute.
  - `Pump 1 Strokes unitless`: Cumulative strokes pump 1.
  - `Pump 2 Strokes unitless`: Pump 2.
  - `Pump 3 Strokes unitless`: Pump 3.
  - `Pump 4 Strokes unitless`: Pump 4.
  - `Total Strokes unitless`: All pumps cumulative.
  - `Pump Time h`: Total pump operating time.

- **Events/Modes/Other**:
  - `TOFB s`: Time on bottom (forward?).
  - `TOBO s`: Time on bottom out.
  - `OSTM s`: On slips time? (from attached, possibly OSTM).
  - `Elapsed time in-slips s`: Time in slips.
  - `SHK3TM_RT min`: Shock time real-time?
  - `Rig Mode unitless`: Current rig activity mode (e.g., drilling, tripping).
  - `SPN Sp_RigMode 2hz unitless`: High-freq rig mode (2Hz sampling).
  - `Pass Name unitless`: Drilling pass identifier.
  - `STUCK_RT unitless`: Stuck pipe real-time flag.
  - `DRET unitless`: Drilling real-time?
  - `EDRT unitless`: Extended drilling real-time?
  - `RHX_RT unitless`: Rotary head exchange?
  - `RGX_RT unitless`: Rotary gear exchange?
  - `AJAM_MWD unitless`: MWD tool status?
  - `BHFG unitless`: Bottom hole flow gradient?
  - `Corr. Drilling Exponent unitless`: Adjusted drilling difficulty index (Bourgoyne-Young model).
  - `nameWellbore`, `name`: Wellbore identifiers (e.g., "15/9-F-9 A - Main Wellbore", "12.25 in Section - MD Log").

Note: Many columns have units (e.g., m, rpm, kPa) appended; some are duplicates or smoothed variants. Unnamed/index columns (e.g., Unnamed: 0) are likely row IDs—drop during cleaning.

### Characteristics
- **Sampling**: Irregular, tied to bit position (e.g., every 0.5-1m advance).
- **Use Cases**: Reservoir characterization, geomechanics, well planning. Ideal for static models like seismic integration.
- **Size**: Smaller files (thousands of rows); sparser than time logs.
- **Example Viz**: Plot Gamma Ray vs. Depth to identify shale/sandstone transitions.

## Time Logs (`time/` folder)
These CSVs capture **real-time** rig and drilling parameters over elapsed time, independent of depth. They're the "heartbeat" of operations. Based on the header from `Norway-NA-15_$47$_9-F-9 A time.csv`, columns overlap with depth logs (e.g., ROP, WOB, gamma) but emphasize time-indexing, with additions like smoothed metrics (30s/5s avgs), survey points (SRV_), real-time pressures (e.g., SPP5s), and volumes. Over 200 columns, high-frequency sampled.

### Typical Columns & Meaning
Grouped with explanations from standard drilling/WITSML terminology:

- **Time-related**:
  - `Time s`: Elapsed time from reference (e.g., spud or log start, in seconds).
  - `MWD Time Stamp s`: Timestamp for MWD data transmission.
  - `DateTime parsed`: Parsed datetime string (e.g., ISO format from log).
  - `Time Time`: Duplicate/alt time column (possibly UTC).
  - `Time chrom sample unitless`: Time of chromatography sample.
  - `Date of Chromatograph Sample unitless`: Date for gas sample.

- **Depth-related** (tracked over time):
  - `Bit Depth m`: Current bit MD.
  - `Bit Depth m.1`: Duplicate bit depth.
  - `Bit Depth (MD) m`: MD of bit.
  - `Total Depth m`: Current total MD.
  - `Lagged Total Depth m`: Lagged TD (for flow-out analysis).
  - `Extrapolated Hole TVD m`: Estimated TVD at current time.
  - `Total Vertical Depth m`: Running TVD.
  - `Hole depth (MD) m`: Current hole MD.
  - `Lag Depth (TVD) m`: TVD for lag samples.
  - `BTVD m`: Bit TVD.
  - `Continuous Survey Depth m`: Depth of latest survey.
  - `DNI_MP m`: Downhole navigation instrument measured point?
  - `SRVDEPTH m`: Survey depth.
  - `SRVTVD m`: Survey TVD.
  - `ESD_DELAY_DEPTH m`: Equivalent static density delay depth.
  - `Chromatograph Sample (TVD) m`: TVD of gas sample.
  - `Depth chrom sample (meas) m`: Measured depth of gas sample.

- **Drilling Dynamics**:
  - `Rate of penetration m/h`: Instantaneous ROP (m/hr).
  - `Rate of Penetration m/h`: Alt/duplicate ROP.
  - `Rate of Penetration (5ft avg) m/h`: 5ft smoothed ROP.
  - `Rate of Penetration 2 minute average m/h`: 2-min smoothed ROP.
  - `1/2ft ROP m/h`: Half-foot ROP.
  - `ROP30s m/h`: 30s average ROP.
  - `Inverse ROP s/m`: Time per meter (1/ROP).
  - `Averaged RPM rpm`: Smoothed RPM.
  - `Average Rotary Speed rpm`: Mean surface RPM.
  - `RPM30s rpm`: 30s avg RPM.
  - `DRPM30s rpm`: Delta RPM 30s?
  - `Total Downhole RPM rpm`: Downhole RPM.
  - `MWD Turbine RPM rpm`: Turbine RPM.
  - `MWD Collar RPM rpm`: Collar RPM.
  - `MWD Stick-Slip PKtoPK RPM rpm`: Stick-slip variation.
  - `Weight on Bit kkgf`: Current WOB.
  - `Averaged WOB kkgf`: Smoothed WOB.
  - `Corrected Surface Weight on Bit kkgf`: Adjusted WOB.
  - `SWOB30s kkgf`: 30s avg surface WOB.
  - `SWOB-DWOB kkgf`: Surface minus downhole WOB.
  - `Average Hookload kkgf`: Mean hook load.
  - `Total Hookload kkgf`: Total hook load.
  - `Corrected Hookload kkgf`: Adjusted hook load.
  - `Corrected Total Hookload kkgf`: Adjusted total.
  - `HKLD30s kkgf`: 30s avg hook load down.
  - `HKLI kkgf`: Hook load in.
  - `HKLO kkgf`: Hook load out.
  - `Weight On Hook kkgf`: Hook weight.
  - `Maximum Hookload kkgf`: Max hook load.
  - `Hookload (min) kkgf`: Min hook load.
  - `"String weight (rot,avg) kkgf"`: Avg rotating string weight.
  - `Averaged TRQ kN.m`: Smoothed torque.
  - `Average Surface Torque kN.m`: Mean surface torque.
  - `TQ30s kN.m`: 30s avg torque.
  - `SIG_TQ30s kN.m`: Signal torque 30s.
  - `Torque loss kN.m`: Torque loss along string.
  - `STOR-DTOR kN.m`: Surface to downhole torque diff.
  - `DTOR*RPM unitless`: Torque * RPM product.
  - `Block Position m`: Height/position of traveling block.
  - `Block Velocity m/s`: Block speed.
  - `Hook Height m`: Hook elevation.
  - `Running speed-down (max) m/s`: Max down speed during trip.
  - `Running speed-up (max) m/s`: Max up speed.
  - `Bit Drill Time h`: Cumulative bit time.
  - `Total Bit Revolutions unitless`: Cumulative revs.
  - `Bit run number unitless`: Bit run count.
  - `On Bottom Status unitless`: 1 if on bottom, 0 off.
  - `Bit on Bottom unitless`: Similar flag.
  - `MWD_BOT unitless`: MWD bottom status.
  - `Trip/Ream/Drill On Bottom Stat unitless`: Activity status.

- **Geological/MWD**:
  - `MWD Raw Gamma Ray 1/s`: Raw gamma counts.
  - `MWD Gamma Ray (API BH corrected) gAPI`: Corrected gamma.
  - `ARC Gamma Ray (BH corrected) gAPI`: ARC gamma.
  - `MWD Continuous Inclination dega`: Inclination.
  - `MWD Continuous Azimuth dega`: Azimuth.
  - `MWD Gravity Toolface dega`: Gravity toolface.
  - `MWD Magnetic Toolface dega`: Magnetic toolface.
  - `MWD GR Bit Confidence Flag %`: Gamma confidence.
  - `MWD TF Bit Confidence Flag %`: Toolface confidence.
  - `MWD Shock Peak m/s2`: Shock peak.
  - `PowerUP Shock Rate 1/s`: Shock rate.
  - `MWD Total Shocks unitless`: Total shocks.
  - `MWD Shock Risk unitless`: Shock risk.
  - `MWD DNI Temperature degC`: Downhole temp.
  - `MWD Transmitted Counts unitless`: Transmitted data counts.
  - `MWD Sync Status unitless`: Sync flag.
  - `MWD Frame Position unitless`: MWD frame pos.
  - `MWD Frame ID unitless`: Frame ID.
  - `MWD DATP ID unitless`: Data packet ID.
  - `MWD_SLIDE unitless`: Sliding mode flag.
  - `MWD Delay Time s`: Transmission delay.
  - `SPR MWD_04 mwd unitless`: MWD signal strength?
  - `DPT_CONF unitless`: Depth confidence.
  - `DNISTAT unitless`: DNI status.
  - `MAG_DEC dega`: Magnetic declination.
  - `TOTAL_CORR dega`: Total correction (magnetic?).
  - `TF_CORR dega`: Toolface correction.
  - `GRID_CORR dega`: Grid correction.
  - `BACC m/s2`: Accelerometer bias.

- **Mud/Fluid & Volumes**:
  - `Mud Density In g/cm3`: In mud weight.
  - `Mud Density Out g/cm3`: Out mud weight.
  - `ECD_MW_IN g/cm3`: ECD at mud in.
  - `ARC Equivalent Circulating Density g/cm3`: Annular ECD.
  - `Mud Flow In L/min`: Flow in rate.
  - `Flow Pumps L/min`: Pump flow.
  - `TFLO30s L/min`: 30s flow avg.
  - `FLOW-TRPM L/min`: Flow per RPM?
  - `TMP In degC`: Pump temp in.
  - `Temperature Out degC`: Out temp.
  - `Annular Temperature degC`: Annular temp.
  - `ARC Annular Pressure kPa`: Annular pressure.
  - `Casing (choke) pressure kPa`: Choke pressure.
  - `SPP-VPWD kPa`: Standpipe minus pore pressure?
  - `SPP-APWD kPa`: SPP minus annular.
  - `SPP5s kPa`: 5s standpipe pressure.
  - `SIG_SPP5s kPa`: Signal SPP 5s.
  - `Stand Pipe Pressure kPa`: SPP.
  - `Average Standpipe Pressure kPa`: Avg SPP.
  - `Fill/gain volume obs. (cum) m3`: Cumulative gains.
  - `Tank volume (active) m3`: Active tank vol.
  - `Tank volume change (active) m3`: Change in active.
  - `Tank 11 Volume m3`: Specific tank.
  - `Trip tank 2 volume m3`: Trip tank.
  - `TripTank Volume 1 m3`: Trip tank 1.
  - `MudPit Volume Average 1-14 m3`: Avg volumes for pits 1-14 (mud monitoring).
  - `Cement flowrate In (avg) m3/min`: Cement flow (if applicable).

- **Pumps & Strokes**:
  - `Pump 1 Stroke Rate 1/min`: Pump 1 SPM.
  - `Pump 2 Stroke Rate 1/min`: Pump 2.
  - `Pump 3 Stroke Rate 1/min`: Pump 3.
  - `Pump 4 Stroke Rate 1/min`: Pump 4.
  - `Total SPM 1/min`: Total SPM.
  - `Pump Speed 1 1/min`: Pump 1 speed.
  - `Pump Speed 2 1/min`: Pump 2.
  - `Pump Speed 3 1/min`: Pump 3.
  - `SPP/SPM2 unitless`: SPP per SPM squared?
  - `TRPM/SPM unitless`: Torque per SPM?
  - `Pump Time h`: Pump hours.
  - `Total Strokes unitless`: Cumulative strokes.

- **Survey (SRV_ metrics - Real-time survey points)**:
  - `SRVDEPTH m`: Survey depth.
  - `SRVTVD m`: Survey TVD.
  - `SRVNS m`: North-south offset.
  - `SRVEW m`: East-west offset.
  - `SRV_HX unitless`: Survey HX (horizontal X?).
  - `SRV_HY unitless`: HY.
  - `SRV_HZ unitless`: HZ.
  - `SRV_GX unitless`: Gravity X.
  - `SRV_GY unitless`: GY.
  - `SRV_GZ unitless`: GZ.
  - `SRVAZI dega`: Survey azimuth.
  - `SRVINC dega`: Survey inclination.
  - `SRVTYPE unitless`: Survey type.
  - `SHX_USL unitless`, `SHY_USL`, `SHZ_USL`, etc.: Survey high/low limits (USL=upper spec limit?).

- **Events/Modes/Status**:
  - `TOFB s`: Time on bottom forward.
  - `TOFF s`: Time off bottom.
  - `TTONB s`: Time to on bottom?
  - `TOJ s`: Time on jars?
  - `Elapsed time in-slips s`: Time in slips.
  - `SHK3TM_RT min`: Real-time shock time.
  - `Rig Mode unitless`: Rig activity (drilling=1, tripping=2, etc.).
  - `Rig Mode unitless.1`: Duplicate.
  - `STUCK_RT unitless`: Stuck flag.
  - `DRET unitless`: Drilling real-time.
  - `EDRT unitless`: Extended DRT.
  - `RGX_RT unitless`: Gear exchange.
  - `RHX_RT unitless`: Head exchange.
  - `Pass Name unitless`: Pass ID.
  - `On Bottom Status unitless`: On bottom flag.
  - `"Slips stat (1=Out,0=In) unitless"`: Slips status.
  - `ATBT unitless`: At bottom?
  - `TRPOUT_CT unitless`: Trip out count.
  - `TRPIN_CT unitless`: Trip in count.
  - `Rotating friction factor unitless`: Friction during rotation.
  - `DRAG sliding friction factor unitless`: Sliding drag.

- **Gas/Chromatography**:
  - `Methane (C1) ppm`: Methane.
  - `Ethane (C2) ppm`: Ethane.
  - `Propane (C3) ppm`: Propane.
  - `Iso-butane (IC4) ppm`: i-Butane.
  - `Nor-butane (NC4) ppm`: n-Butane.
  - `Iso-pentane (IC5) ppm`: i-Pentane.
  - `n-Penthane ppm`: n-Pentane.
  - `Gas (avg) %`: Avg gas.

- **Other/Misc**:
  - `MWD Sync Status unitless`: Sync.
  - `CUREDT_RT unitless`: Corrected EDT real-time.
  - `BHFG unitless`: Bottom hole FG.
  - `AJAM_MWD unitless`: MWD status.
  - `nameWellbore`, `name`: Identifiers.
  - `WBSLITHOLOGY1-5 unitless`: Lithology mnemonics.
  - `WBSTRAJECTORYMNEMONIC`, etc.: Wellbore schema mnemonics (e.g., caliper, bit dep, tubular).
  - Real-time pressures: `"Static Pressure, Real-Time kPa"`, `"Maximum Static Pressure, Real-Time kPa"`, etc. (for pore/static equiv).
  - `PMAX_TM_RT unitless`, `PMIN_TM_RT`: Pressure max/min time real-time.
  - `PESD_TM_RT unitless`: Pore equiv static density time.

Note: Smoothing (e.g., 30s, 5s) for noise reduction in high-freq data; SRV_ for continuous surveying; many duplicates/RT variants for real-time monitoring.

### Characteristics
- **Sampling**: High-frequency (e.g., 1-10 seconds intervals), continuous during active drilling.
- **Use Cases**: Real-time optimization, anomaly detection (e.g., vibrations via torque spikes), predictive maintenance (e.g., bit wear from ROP drop). Great for time-series ML like LSTM for stuck pipe prediction.
- **Size**: Larger files (millions of rows); dense, noisy (outliers from sensor glitches).
- **Example Viz**: Plot ROP vs. Time to spot efficiency drops during connections; correlate with mud weight changes.

## Why the Split?
- **Data Nature**: Depth logs are position-based (geology-focused, lower freq); time logs are event-based (ops-focused, high freq). Merging requires interpolation (e.g., using bit position to map time to depth).
- **Efficiency**: Separate processing pipelines—depth for static analysis, time for dynamic forecasting.
- **WITSML Origin**: Standard export groups logs by log type (mnemonic: `MNEM` for depth vs. real-time channels).
- **Common Pitfalls**: Timestamps may need timezone conversion (UTC to local); depth files lack time context, time files lack precise geology.

## Usage Tips for EDA/ML
- **Loading**: Use `fireducks.pandas` or `polars` for big CSVs (handles mixed types). Set `low_memory=False`, `on_bad_lines="skip"`. Preview with `df.head()` and `df.dtypes`.
- **Cleaning**: 
  - Parse timestamps: `pd.to_datetime(df['RIG TIME'], utc=True)`.
  - Handle mixed cols: Specify dtypes (e.g., `{'Lithology': str, 'ROP': float}`).
  - Resample time data: Downsample to 1-min for viz (e.g., `df.resample('1T', on='TIMESTAMP').mean()`).
- **Merging**: Join on nearest depth/time via `scipy.interpolate` or well trajectory logs.
- **EDA Steps**:
  1. Load one time CSV: Check for ROP, pressure trends.
  2. Load depth CSV: Inspect gamma/resistivity profiles.
  3. Stats: `df.describe()`, missingness `df.isnull().sum()`.
  4. Viz: Seaborn/Matplotlib for correlations (e.g., ROP vs. WOB).
- **ML Ideas**: 
  - Time: Predict ROP from params (Random Forest/XGBoost).
  - Depth: Classify lithology from logs (CNN on profiles).
  - Combined: Anomaly detection in real-time streams.
- **Resources**: 
  - Volve Dataset: [Equinor Volve Portal](https://data.equinor.com/dataset/volve).
  - WITSML Spec: [Energistics.org](https://www.energistics.org/standards/witsml).
  - Drilling Basics: SPE papers on ROP optimization.

For questions on specific wells/files, run `df.info()` and share column names.

---
*Last Updated: Oct 2025 | Based on Volve WITSML CSVs v1.0*
