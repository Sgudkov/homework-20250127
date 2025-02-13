# Log Analyzer
================

The Log Analyzer is a Python script designed to process log files and generate reports in HTML format. The script reads log files, parses the data, and produces a report that provides insights into URL access patterns.


## Functionality

The Log Analyzer performs the following functions:

- Reads log files in gzip format
- Parses log data and extracts relevant information
- Generates reports in HTML format
- Produces reports that include URL access patterns, such as count, percentage, time sum, time percentage, time average, time maximum, and time median
- Limits reports to the first `REPORT_SIZE` lines
- Sorts reports by time percentage in descending order

## Configuration

The Log Analyzer uses a configuration file (`conf.json`) to set report size, report directory, and log directory.

### Configuration Options

- `REPORT_SIZE`: The maximum number of lines to include in the report.
- `REPORT_DIR`: The directory where the report will be saved.
- `LOG_DIR`: The directory where the log files are located.

### Example Configuration File (`conf.json`)

```json
{
    "REPORT_SIZE": 2000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log"
}
```

## Report

The report is generated in HTML format and includes the following information:

- URL access patterns, including count, percentage, time sum, time percentage, time average, time maximum, and time median
- The report is sorted by time percentage in descending order
- The report is limited to the first `REPORT_SIZE` lines

## Usage

To use the Log Analyzer, simply execute the `log_analyzer.py` script and provide the path to your log file as a command-line argument.

Example usage:

```bash
python log_analyzer.py -c conf.json
