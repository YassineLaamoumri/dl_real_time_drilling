# Data Area

This directory holds datasets and documentation.

- `raw/`: immutable source files (never edit in place)
- `interim/`: temporary working files during preprocessing
- `processed/`: curated datasets ready for training/serving

## Schemas

See typical CSV columns below. Normalize units at ingestion time.

### Time-based CSV
- timestamp (ISO8601 or epoch ms)
- hookload (kN)
- rpm (rev/min)
- torque (kNm)
- flow (m3/h)
- spm (strokes/min)
- standpipe_pressure (bar)
- wob (kN)
- bit_depth (m)
- hole_depth (m)
- rop (m/h)

### Depth-based CSV
- md (m)
- tvd (m)
- rop (m/h)
- wob (kN)
- rpm (rev/min)
- torque (kNm)
- spp (bar)
- flow (m3/h)

