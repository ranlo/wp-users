import sys
import requests
import csv
import re
import argparse

def get_wordpress_users_info(domain, no_header=False):
    # Initialize variables for pagination
    page = 1
    per_page = 50
    has_next_page = True

    # Open a CSV file for writing
    with open(f"{domain}_users.csv", mode='w', newline='') as csv_file:
        # Create a CSV writer
        csv_writer = csv.writer(csv_file)

        while has_next_page:
            # Check if there is a WordPress users page
            users_url = f"https://{domain}/wp-json/wp/v2/users?page={page}&per_page={per_page}"
            response = requests.get(users_url)

            # Check for HTTP errors
            response.raise_for_status()

            if response.status_code == 200:
                users_data = response.json()

                # Output CSV header if it's the first page
                if page == 1 and not no_header:
                    csv_writer.writerow(["Domain", "Name", "Slug", "Gravatar Hash"])

                for user in users_data:
                    # Extract name, slug, and hash from Gravatar URL if available
                    avatar_urls = user.get('avatar_urls', {})
                    gravatar_url = avatar_urls.get('96', '')  # Assuming '96' is the size you want
                    match = re.search(r"/avatar/([a-f0-9]+)", gravatar_url)

                    if match:
                        hash_value = match.group(1)
                    else:
                        hash_value = "N/A"  # No Gravatar hash found

                    name = user.get('name', '')
                    slug = user.get('slug', '')

                    # Write to CSV file
                    csv_writer.writerow([domain, name, slug, hash_value])

                # Print feedback
                print(f"Processed page {page}")

                # Check for the next page
                link_header = response.headers.get('link', '')
                has_next_page = 'rel="next"' in link_header
                page += 1

            else:
                print(f"Error accessing {domain}. Status code: {response.status_code}")
                break

    print(f"Processing for {domain} completed. CSV file saved as {domain}_users.csv")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Get WordPress user information from a domain.")
    parser.add_argument("domain", help="The domain name to check for WordPress users.")
    parser.add_argument("--no-header", action="store_true", help="Do not include a header in the CSV file.")

    args = parser.parse_args()

    # Validate domain name (optional)
    # You may want to add additional validation based on your requirements

    print(f"Processing users for {args.domain}...")

    get_wordpress_users_info(args.domain, args.no_header)
