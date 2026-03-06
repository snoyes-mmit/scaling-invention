# URL Validator

A robust Python application for validating URLs extracted from Excel files. Designed to handle large-scale URL validation with concurrency control, rate limiting, and retry logic to avoid server throttling and ensure reliable results.

## Features

- **Concurrent Validation**: Processes multiple URLs simultaneously with configurable concurrency limits.
- **Rate Limiting**: Built-in delays between requests to prevent overwhelming servers.
- **Retry Logic**: Automatic retries on failures with exponential backoff.
- **Efficient Networking**: Uses HEAD requests first (fallback to GET) and connection reuse.
- **Resilient Design**: Handles timeouts, redirects, and various HTTP errors gracefully.
- **Flexible Input/Output**: Scans all cells in Excel files to find URLs automatically.
- **Comprehensive Results**: Outputs detailed validation status, HTTP codes, response times, redirects, and error messages with location information.
- **Prioritized Output**: Failed URLs are listed first with verbose error explanations, followed by valid URLs.
- **Location Tracking**: Includes sheet, row, and column information for each URL found.

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone or download the project files.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Graphical User Interface (GUI)

For non-technical users, use the GUI application:

```bash
python gui.py
```

This opens a window where you can:
- Browse and select the input Excel file
- Choose the output file location
- Set concurrency and rate limit options
- Click "Validate URLs" to run the validation
- View progress and results in the output area

The application will automatically scan all cells in the Excel file for URLs.

### Command Line Interface

#### Basic Usage

```bash
python url_validator.py input.xlsx
```

This will:
- Scan all cells in `input.xlsx` for URLs
- Validate each URL with default settings
- Save results to `validated_urls.xlsx`

#### Advanced Usage

```bash
python url_validator.py input.xlsx --output results.xlsx --concurrency 5 --rate_limit 0.2
```

### Command Line Options

- `input_file`: Path to the input Excel file (.xlsx) containing URLs. (Required)
- `--output`: Path for the output Excel file. Default: 'validated_urls.xlsx'
- `--concurrency`: Maximum number of concurrent requests. Default: 10
- `--rate_limit`: Delay in seconds between requests. Default: 0.1

### Input File Format

The input Excel file can contain URLs anywhere in the spreadsheet. The application will scan all cells in all sheets and extract any text that matches URL patterns (starting with http:// or https://).

Supported formats:
- .xlsx files
- URLs can be in any cell, mixed with other text
- Multiple URLs per cell are supported
- The application processes all sheets in the workbook

Example input.xlsx (Sheet1):

| Name | Description | Links |
|------|-------------|-------|
| Site A | Check this out | https://example.com |
| Site B | Multiple links | https://google.com and https://bing.com |

Example input.xlsx (Sheet2):

| Data |
|------|
| Visit https://website.com for more info |
| Invalid text here |

### Output File Format

The output Excel file contains the following columns, with failed URLs listed first and valid URLs at the bottom:

- **url**: The original URL
- **sheet**: The sheet name where the URL was found
- **row**: The row number where the URL was found (1-based)
- **column**: The column number where the URL was found (1-based)
- **cell_value**: The full text content of the cell containing the URL
- **status**: 'valid', 'invalid', or 'error'
- **http_code**: HTTP status code (e.g., 200, 404) or None for errors
- **response_time**: Time taken for the request in seconds (rounded to 2 decimals) or None for errors
- **redirect**: Final URL if redirected, otherwise None
- **error**: Detailed explanation of why the URL failed validation, otherwise None

Failed URLs (status 'error' or 'invalid') appear first in the output, followed by valid URLs. Error messages provide verbose explanations of the failure reasons.

Example output:

Example output:

| url                 | sheet | row | column | cell_value              | status | http_code | response_time | redirect | error |
|---------------------|-------|-----|--------|-------------------------|--------|-----------|---------------|----------|-------|
| https://website.com | Sheet2| 1   | 1      | Visit https://website.com for more info | invalid| 404       | 0.02          | None     | Page not found (404): The requested URL does not exist on the server. The page may have been moved, deleted, or the URL is incorrect. |
| https://broken.com  | Sheet1| 4   | 2      | https://broken.com      | error  | None      | None          | None     | Connection timeout: The server did not respond within the allowed time (10 seconds). This could indicate server overload, network issues, or the server is down. |
| https://example.com | Sheet1| 2   | 3      | Check this out https://example.com | valid  | 200       | 0.15          | None     | None  |
| https://google.com  | Sheet1| 3   | 3      | https://google.com and https://bing.com | valid  | 200       | 0.12          | https://www.google.com | None  |
| https://bing.com    | Sheet1| 3   | 3      | https://google.com and https://bing.com | valid  | 200       | 0.08          | None     | None  |

## Configuration Tips

### Handling Large Datasets

For large Excel files (10k+ URLs):
- Reduce concurrency: `--concurrency 5`
- Increase rate limit: `--rate_limit 0.5`
- Monitor system resources

### Avoiding Blocks

- Use appropriate rate limits based on target server policies
- Distribute validation over time if needed
- Respect robots.txt and terms of service

### Timeouts and Retries

- Default timeout: 10 seconds per request
- Retries: Up to 3 attempts with exponential backoff (1s, 4s, 10s delays)

## Architecture Notes

This application implements production-grade URL validation:

- **Concurrency Control**: Semaphore limits simultaneous requests
- **Rate Limiting**: Configurable delays prevent server overload
- **Retry Strategy**: Tenacity library handles transient failures
- **HTTP Efficiency**: HEAD requests minimize bandwidth
- **Error Handling**: Comprehensive exception catching and logging

## Troubleshooting

- **Import Errors**: Ensure all dependencies are installed via `pip install -r requirements.txt`
- **File Not Found**: Check input file path and permissions
- **No URLs Found**: Verify that your Excel file contains URLs starting with http:// or https://
- **Network Issues**: Check internet connection and firewall settings
- **Large Files**: For very large datasets, consider splitting the input file

## Contributing

To extend the application:
- Add more validation checks (e.g., SSL verification)
- Support additional input formats (CSV, JSON)
- Implement progress bars for long-running validations
- Add logging to files for better debugging

## License

This project is open-source. Use at your own risk.