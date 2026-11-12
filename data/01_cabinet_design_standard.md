# Control Cabinet Design Standard (DAS-EL-01)

> Fictional sample document of Demo Automation GmbH, written for a software demo. Not a real design rule.

## Scope
This standard applies to all low-voltage control cabinets (up to 690 V AC) that Demo Automation GmbH designs for conveyor and baggage handling systems. Deviations must be approved by the lead electrical engineer and documented in the project's change log.

## Spare space and reserves
Every new cabinet must keep at least 20 % free mounting-plate space and at least 20 % free space in the wire ducts at handover. DIN rails should have at least 15 % free length per rail. PLC I/O reserves are defined in the PLC I/O conventions (DAS-EL-04).

## Layout of the mounting plate
- Main switch (-Q1) and incoming supply terminals are placed at the top left.
- Power section (circuit breakers, motor starters, frequency inverters) is placed in the upper part, control section (PLC, relays, 24 V power supplies) in the lower part.
- Frequency inverters are mounted with the manufacturer's minimum clearance above and below (normally 100 mm) for airflow.
- Power cables and 24 V signal cables must run in separate wire ducts. If they cross, they cross at 90°.
- Terminal strips (-X) are placed at the bottom edge so that field cables enter from below.

## Thermal design
A heat calculation is required for every cabinet. The internal temperature must not exceed 35 °C at an ambient temperature of 30 °C. If the calculation shows more than 35 °C, a filter fan is required; above 40 °C a cooling unit must be used. The heat calculation report is stored with the project documentation.

## Protective earth (PE)
Every metallic door, mounting plate and side panel is connected to the PE busbar with a green-yellow earthing strap of at least 6 mm². Doors with mounted devices need their own PE connection. The PE busbar is marked "PE" and is placed next to the incoming supply terminals.

## Door devices
Emergency stop push buttons, the main switch handle and indicator lamps are placed on the door between 0.6 m and 1.7 m above floor level. The emergency stop button is red on a yellow background.

## Labelling
All devices carry a label with their reference designation (see DAS-EL-03), both on the device and on the mounting plate below it. Labels are white with black text, printed, never handwritten. Cabinets carry a rating plate with project number, rated voltage, rated current, short-circuit rating and year of manufacture.
