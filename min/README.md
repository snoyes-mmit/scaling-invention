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

## Standalone Application

For non-technical users, a packaged executable is available that doesn't require Python installation or command line usage.

### Creating the Executable

If you have Python installed:

1. Install PyInstaller: `pip install pyinstaller`
2. Run: `pyinstaller --onefile --windowed gui.py --add-data "url_validator.py;."`
3. The executable `gui.exe` will be created in the `dist` folder.

### Using the Standalone App

1. Copy `gui.exe` from the `dist` folder to your desktop or preferred location.
2. Rename it to `URL Validator.exe` for clarity.
3. Double-click the executable to launch the application.
4. The GUI will open, allowing you to select files and configure settings without any terminal commands.

**Note**: The standalone executable includes all necessary dependencies and can be run on any Windows computer without installing Python.

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

## Concurrency and Rate Limiting

### Max Concurrency

The maximum concurrency setting controls how many URL validation requests are processed simultaneously. The default value is 10 concurrent requests.

**Maximum Value**: There is no hard-coded upper limit in the application, but practical limits depend on your system's resources and network capabilities. Typically, values between 5-50 are reasonable for most systems. Extremely high values (100+) may lead to system resource exhaustion, network congestion, or being blocked by target servers.

**When to Increase Concurrency**:
- When validating URLs from fast-responding servers
- When your local network and system have sufficient bandwidth and CPU resources
- When processing large batches and time is a critical factor
- When target servers have high capacity and don't enforce strict rate limits

**When to Decrease Concurrency**:
- When encountering frequent timeouts or connection errors
- When servers return HTTP 429 (Too Many Requests) status codes
- When your network connection is slow or unstable
- When validating URLs from servers with known rate limiting policies
- When system resources (CPU, memory) are being heavily utilized

### Rate Limiting

Rate limiting introduces a delay between individual URL validation requests to prevent overwhelming target servers. The default rate limit is 0.1 seconds (100ms) between requests.

**How It Works**: Each concurrent task waits for the specified delay before making a request. With the default concurrency of 10 and rate limit of 0.1s, this allows approximately 100 requests per second total (10 concurrent × 10 requests/second each).

**How to Set the Rate Limit**:
- **Command Line**: Use the `--rate_limit` parameter followed by the delay in seconds (e.g., `--rate_limit 0.5` for 500ms delay)
- **GUI**: Enter the desired delay in seconds in the "Rate Limit (seconds)" field (default: 0.1)

**Recommended Values**:
- **Fast networks/servers**: 0.05 - 0.1 seconds (200-10 requests/second per concurrent task)
- **Standard usage**: 0.1 - 0.2 seconds (10-5 requests/second per concurrent task)
- **Conservative/slow servers**: 0.5 - 1.0 seconds (2-1 requests/second per concurrent task)
- **Very restrictive servers**: 2.0+ seconds (0.5 requests/second or slower per concurrent task)

**Note**: The effective request rate is concurrency × (1 / rate_limit). For example, concurrency=5 with rate_limit=0.2 results in 25 requests per second total.

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

### Performance and Runtime Estimates

#### Key Factors Affecting Runtime
- **Network Conditions**: Response times vary widely (0.1-5+ seconds per URL depending on server speed and your internet connection)
- **Failure Rate**: Failed URLs trigger retries (up to 3 attempts with 1s, 4s, and 10s delays between attempts), significantly increasing time
- **Concurrency Settings**: Default is 10 concurrent requests
- **Rate Limiting**: Default 0.1s delay between requests
- **Excel File Size**: Initial scanning of all cells to extract URLs can take 1-5 minutes for large files
- **System Resources**: CPU, memory, and local network speed

#### Estimated Runtime Ranges

**With Default Settings (Concurrency: 10, Rate Limit: 0.1s)**:
- **Optimistic scenario** (fast servers, low failure rate): 30-60 minutes
- **Typical scenario** (mixed response times, 10-20% failures): 1-2 hours
- **Conservative scenario** (slow servers, high failure rate): 2-4 hours

**With Recommended Large-Dataset Settings (Concurrency: 5, Rate Limit: 0.5s)**:
- **Optimistic scenario**: 1-2 hours
- **Typical scenario**: 2-4 hours
- **Conservative scenario**: 4-8 hours

#### Why These Estimates?
- **Concurrent Processing**: With 10 concurrent requests, the application processes ~10 URLs every 0.5-1 second (depending on response times)
- **Sequential Bottlenecks**: Rate limiting and retries create sequential delays that can't be fully parallelized
- **Real-World Variance**: Actual times vary greatly based on target server performance and network quality

#### Recommendations for Large Datasets
- **Start with conservative settings**: Use `--concurrency 5 --rate_limit 0.5` to avoid overwhelming servers
- **Monitor progress**: The application prints progress updates during execution
- **Split large jobs**: Consider processing in batches of 10,000-20,000 URLs if possible
- **Network considerations**: Run during off-peak hours if targeting specific servers
- **Test first**: Validate a small sample (100-1000 URLs) to estimate timing for your specific URLs

For 80,000+ URLs, expect at least 1-2 hours under typical conditions, but plan for up to 4-8 hours in worst-case scenarios with high failure rates or slow networks. The application is designed to be resilient rather than fast, prioritizing reliability over speed.

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