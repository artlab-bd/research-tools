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

## License

Released under the MIT License.
