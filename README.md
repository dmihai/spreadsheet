# spreadsheet

This is a solution for the staking-rewards backend challenge: https://github.com/stakingrewards/engineering-challenge/tree/backend

## Setup

You have to install python on your machine if you don't have it already.

## Usage

This is a CLI tool that processes the input CSV file you specify and writes the result to another CSV file. You can run it like so:

```bash
py main.py --input=transactions.csv --output=result.csv
```

If you do not specify an input and/or an output value they default to:

- input = transactions.csv
- output = output.csv
