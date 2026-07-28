# Crime Dataset Data Contract

## Purpose

Defines the expected structure of the crime dataset used by the dashboard.

## Required Columns

| Column | Type | Description |
|---|---|---|
| State | string | Australian state or territory |
| Year | integer | Reporting year |
| Offence | string | Crime category |
| Count | integer | Number of recorded offences |

## Validation Rules

- State cannot be empty
- Year must be between 1900 and current year
- Count cannot be negative
- Offence category cannot be empty

## Assumptions

- Data represents reported offences
- Data may differ between jurisdictions