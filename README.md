# WordPress User Exporter

This script extracts user information from a WordPress-powered website and saves it to a CSV file. It is useful for security researchers or administrators who want to get a quick overview of the users on a specific WordPress site.

## Requirements

*   Python 3
*   `requests` library

## Installation

1.  Make sure you have Python 3 installed on your system.
2.  Install the required `requests` library using pip:

    ```bash
    pip install requests
    ```

## Usage

To use the script, run it from the command line:

```bash
python3 get_domain_users.py [-h] [--no-header] domain
```

### Arguments

*   `domain`: The domain name of the WordPress site to scan.
*   `-h`, `--help`: Show a help message and exit.
*   `--no-header`: Do not write a header row in the CSV output file.

The script will create a CSV file named `<domain>_users.csv` in the same directory.

### Example

**Standard Usage**

To get users from `example.com` and save them to `example.com_users.csv` with a header row:

```bash
python3 get_domain_users.py example.com
```

**No-Header Mode**

To get users from `example.com` but without a header row in the CSV:

```bash
python3 get_domain_users.py example.com --no-header
```

## How It Works

The script leverages the public WordPress REST API to fetch user data. Specifically, it makes requests to the `/wp-json/wp/v2/users` endpoint. It then parses the JSON response and extracts the relevant user information.

## CSV Output

The output CSV file (`<domain>_users.csv`) will have the following columns:

*   **Domain**: The target domain name.
*   **Name**: The display name of the user.
*   **Slug**: The user's slug (URL-friendly name).
*   **Gravatar Hash**: The MD5 hash of the user's email address, extracted from their Gravatar URL. This can be useful for cross-referencing users across different platforms.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.
