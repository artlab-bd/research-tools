# ART Lab Research Tools

Open research, monitoring, evaluation and data tools from
[ART Lab](https://artlab-bd.com/).

## CSV Quality Check

`csv_quality_check.py` reviews a CSV dataset and reports:

- total rows and columns;
- duplicate rows;
- missing values by column; and
- completely empty rows.

It uses only the Python standard library.

```bash
python csv_quality_check.py data.csv
```

Save the report as JSON:

```bash
python csv_quality_check.py data.csv --json report.json
```

Try the included fictional dataset:

```bash
python csv_quality_check.py examples/fictional_survey.csv
```

The example intentionally contains a duplicate record, missing values and an
empty row. It contains no client or participant data.

## Test

Run the standard-library test suite from the repository root:

```bash
python -m unittest discover -s tests -v
```

## Responsible use

This checker is an initial diagnostic, not a complete data-quality protocol.
Review instrument logic, identifiers, ranges, skip patterns, consent rules and
project-specific definitions before analysis. Never publish confidential data
or a generated report containing sensitive file paths or field names.

## License

Released under the MIT License.
