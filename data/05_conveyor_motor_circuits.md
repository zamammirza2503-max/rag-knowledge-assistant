# Conveyor Motor Circuits (DAS-EL-05)

> Fictional sample document of Demo Automation GmbH, written for a software demo. Not a real design rule.

## Typical drives
Baggage handling conveyors normally use three-phase asynchronous gear motors between 0.37 kW and 4 kW at 400 V AC. Conveyors that need speed control or soft start (merges, high-speed belts, sorter infeeds) use a frequency inverter. Simple transport conveyors may use direct-on-line starting with a motor starter.

## Direct-on-line motors
A direct-on-line conveyor motor is fed by a motor protection switch (-F) with an adjustable overload release set to the motor's rated current, followed by a contactor (-Q) controlled by the PLC. Alternatively, a combined motor starter (-Q) can be used. The overload setting is documented in the schematic next to the device.

## Motors with a frequency inverter
- Each frequency inverter (-T) is protected by the circuit breaker or fuse type and rating specified in the inverter manufacturer's manual. The motor protection function is provided by the inverter parameters, so no separate motor protection switch is needed between inverter and motor.
- The motor cable is shielded, with the shield connected at both ends over 360°.
- The inverter's Safe Torque Off (STO) input is used for emergency stop. STO is wired from the safety relay or safety PLC, never from standard PLC outputs.
- The maximum motor cable length given by the inverter manufacturer must be respected; above 50 m an output choke may be required.

## Emergency stop
Conveyor sections are grouped into emergency stop zones. Pressing an emergency stop removes the torque of all drives in its zone. Drives with frequency inverters use stop category 1 (controlled braking, then STO); direct-on-line drives use stop category 0 (immediate removal of power via the contactor).

## Repair switches
Every conveyor motor in the field has a lockable repair switch near the motor, so maintenance staff can isolate it safely. For motors on frequency inverters, the repair switch must have an auxiliary contact that is read by the PLC, so the inverter is disabled before the switch opens.
