# Delta Lake Tables (NHRIS)

## patient_events
Raw cleaned patient-level events.

Columns:
- timestamp (string, ISO)
- heart_rate (int)
- oxygen_level (int)
- temperature (double)
- blood_pressure (string)
- patient_location (string)
- diagnosis (string)
- region (string)
- city (string)
- bp_systolic (int)
- bp_diastolic (int)

Storage:
- `delta/patient_events`

## regional_aggregates
Aggregated by region/city/diagnosis.

Columns:
- region (string)
- city (string)
- diagnosis (string)
- case_count (long)
- avg_temperature (double)
- avg_oxygen (double)
- max_heart_rate (int)
- run_ts (string)

Storage:
- `delta/regional_aggregates`

## alerts
Detected alerts for outbreak/risk.

Columns:
- region (string)
- city (string)
- diagnosis (string)
- case_count (long)
- alert_reason (string)

Storage:
- `delta/alerts`
