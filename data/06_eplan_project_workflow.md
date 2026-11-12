# EPLAN Project Workflow and Release Process (DAS-EL-06)

> Fictional sample document of Demo Automation GmbH, written for a software demo. It describes our own internal process, not EPLAN's product documentation.

## Starting a project
Every new project is created from the company project template, which contains the page structure, title block, report templates and the reference designation settings described in DAS-EL-03. Projects are named with the customer project number, e.g. "P24017_Airport_BHS".

## Parts and macros
Only parts from the company part master data may be placed in a project. If a part is missing, the engineer requests it from the parts management team; parts are never created locally inside a project. Recurring circuits (for example a conveyor motor with inverter, or a 24 V supply group) are placed from approved macros, so that devices, wiring and parts are consistent.

## Generated reports
Bill of materials, terminal diagrams, cable lists, I/O lists and the device tag list are generated automatically from the schematic. Generated reports must never be edited by hand; if something is wrong in a report, the schematic or the part data is corrected and the report is regenerated.

## Checks before release
Before a project revision can be released:
1. The automatic project check runs without errors. Warnings must be reviewed and either fixed or justified in the check log.
2. All protective devices are checked against the cable cross-sections (DAS-EL-02).
3. The heat calculation for each cabinet is attached (DAS-EL-01).
4. A second engineer reviews the schematic (four-eyes principle) and signs the review checklist.
5. All reports are regenerated after the last change.

## Revisions and change requests
Released revisions are numbered A, B, C... Changes after release require a change request (CR) with a description, the affected reference designations and the reason. Changed pages are marked with a revision cloud and the revision letter. The PLC software team is informed about every CR that changes the I/O list.

## Handover
The released project is exported as PDF for the customer and as a project archive for the internal file server. Manufacturing receives the bill of materials, wire list and terminal diagrams of the same revision.
