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

To use the script, run it from the command line and provide the domain name of the WordPress site as an argument:

```bash
python3 get_domain_users.py <domain>
```

Replace `<domain>` with the actual domain name you want to target (e.g., `example.com`).

The script will create a CSV file named `<domain>_users.csv` in the same directory.

### Example

```bash
python3 get_domain_users.py example.com
```

This will generate a file named `example.com_users.csv` with the user data from that site.

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
