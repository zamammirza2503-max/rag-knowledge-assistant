# Wiring and Cable Guideline (DAS-EL-02)

> Fictional sample document of Demo Automation GmbH, written for a software demo. Values are simplified house values, not a substitute for the applicable standards.

## Wire colours inside the cabinet
Demo Automation follows the usual colour scheme for machine wiring:
- Black: AC and DC main power circuits
- Red: AC control circuits (e.g. 230 V AC)
- Dark blue: DC control circuits (24 V DC)
- Orange: interlock circuits supplied from an external source (remain live when the main switch is off)
- Green-yellow: protective earth (PE) only
- Light blue: neutral conductor (N)

Green-yellow must never be used for any other purpose.

## Minimum cross-sections
- Power circuits: minimum 1.5 mm² copper.
- 24 V DC control wiring inside the cabinet: 0.75 mm².
- Signal wiring to PLC inputs inside the cabinet: 0.5 mm² is allowed.
- PE conductors: same cross-section as the phase conductor up to 16 mm².

## Cross-section and protective device (house values)
The protective device (circuit breaker or fuse) must protect the cable against overload. For copper PVC wires in a wire duct inside the cabinet, use these maximum ratings:

| Cross-section | Max. protective device |
|---|---|
| 0.75 mm² | 6 A |
| 1.0 mm² | 10 A |
| 1.5 mm² | 16 A |
| 2.5 mm² | 20 A |
| 4 mm² | 25 A |
| 6 mm² | 32 A |
| 10 mm² | 50 A |
| 16 mm² | 63 A |

Example: a 16 A breaker needs at least 1.5 mm²; a 20 A breaker needs at least 2.5 mm². For bundled cables or ambient temperatures above 40 °C the lead engineer must check derating factors.

## Voltage drop
The voltage drop from the cabinet to a motor or consumer must not exceed 3 % of the rated voltage. For long conveyor lines (more than 50 m cable length) the voltage drop must be calculated and documented. If the limit is exceeded, choose the next larger cross-section.

## Field cables and naming
Field cables carry the designation -W followed by a number, for example -W101. Motor cables from frequency inverters must be shielded, and the shield is connected over 360° with an EMC cable gland at the cabinet entry. Each cable is listed in the automatically generated cable list with source, target, type, cross-section and length.

## Ferrules and terminals
Every stranded wire end gets a ferrule. Spring-clamp terminals are preferred. Maximum two wires per terminal point, and only with twin ferrules.
