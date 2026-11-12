# PLC and I/O Conventions (DAS-EL-04)

> Fictional sample document of Demo Automation GmbH, written for a software demo.

## I/O reserves
Every PLC station must have at least 15 % spare digital inputs, 15 % spare digital outputs and at least one free slot on the rack or bus coupler at handover. Spare channels are wired to terminals and marked "SPARE" in the schematic.

## I/O list
An I/O list is generated automatically from the schematic for every project. It contains: PLC address, symbol name, reference designation of the connected device, description and signal type. The I/O list is the binding interface to the PLC software team. Changes to I/O assignments after the I/O list is released require a change request.

## Symbol names
PLC symbol names are built from the function aspect and the device tag, for example "BHS1_CONV03_B12_PhotoEye". Only letters, numbers and underscores are allowed.

## Supply of I/O modules
Inputs and outputs are supplied from separate 24 V DC circuits, each protected by its own circuit breaker. Outputs of one I/O module are protected with a maximum of 4 A per group. Sensors in the field are supplied via -F protected 24 V circuits with a maximum of 2 A per group.

## Safety I/O
Safety-related signals (emergency stop, safety doors, light curtains) are connected only to safety-rated I/O modules or safety relays. They are never connected to standard I/O. Safety circuits are documented on separate schematic pages marked "SAFETY".
