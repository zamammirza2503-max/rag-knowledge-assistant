# Reference Designation Guide (DAS-EL-03)

> Fictional sample document of Demo Automation GmbH, written for a software demo. The structure follows the principles of IEC 81346; the letter codes below are our simplified house convention.

## Structure of a reference designation
Every device in a schematic has a unique reference designation made of three aspects:
- **=** function aspect: which plant section or function the device belongs to, e.g. =BHS1 (baggage handling system, section 1) or =CONV03 (conveyor 3).
- **+** location aspect: where the device is installed, e.g. +CAB2 (control cabinet 2) or +FIELD (in the field).
- **-** product aspect: what the device is, made of a letter code and a running number, e.g. -K12.

Example: **=BHS1+CAB2-K12** is relay or contactor K12, installed in cabinet 2, belonging to baggage handling section 1.

## Letter codes (house convention)
| Code | Meaning | Examples |
|---|---|---|
| -A | assemblies and controllers | PLC CPU, I/O modules, safety relay |
| -B | sensors | photo eyes, proximity switches, encoders |
| -F | protective devices | circuit breakers (MCB), fuses, motor protection switches |
| -K | relays and contactors for control | coupling relays, auxiliary contactors |
| -M | motors | conveyor drive motors, fans |
| -P | indicators | indicator lamps, horns |
| -Q | power switching | main switch, motor contactors, motor starters |
| -S | manual operation | push buttons, selector switches, emergency stop |
| -T | converting energy | 24 V power supplies, transformers, frequency inverters |
| -W | cables | field cables, motor cables |
| -X | connecting | terminal strips, plug connectors |

## Numbering rules
Numbers are unique within a cabinet. Devices are numbered by schematic page: devices on page 12 use numbers 12x where possible (e.g. -F121, -K122). Numbers of deleted devices are not reused within the same project revision.

## Terminals and wires
Terminal strips are named -X1, -X2 ... and terminal points are numbered from 1 upwards, e.g. -X2:14. Wire numbers follow the potential, e.g. all 24 V DC wires are named "24V", all 0 V wires "0V".
