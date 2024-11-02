#!/usr/bin/env python3
# encoding: UTF-8

"""
    This file is part of MailMiner
    Copyright (C) 2024 @VirajMadhu
    https://github.com/VirajMadhu/MailMiner
    
    MailMiner is a robust Python tool designed for efficiently extracting 
    email addresses from websites. You can input a 
    list of URLs, and MailMiner will dig through each site, uncovering unique 
    email addresses quickly. Perfect for marketers, researchers, and anyone in
    need of targeted email collection! 

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    For more see the file 'LICENSE' for copying permission.
"""

__author__ = "VirajMadhu"
__copyright__ = "Copyright (C) 2024 @VirajMadhu"
__credits__ = ["VirajMadhu"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "VirajMadhu"

################################

import re
import urllib.request
import time

# Email regex pattern
emailRegex = re.compile(r'''
    [a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+
''', re.VERBOSE)

# Extract emails from page text
def extract_emails_from_text(text, email_file):
    extracted_emails = set(emailRegex.findall(text))
    print(f"\tNumber of Emails Found: {len(extracted_emails)}")
    for email in extracted_emails:
        email_file.write(email + "\n")

# Read HTML page content
def fetch_html_content(url, email_file, index):
    start_time = time.time()
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request) as response:
            page_content = response.read().decode('utf-8', errors='ignore')
            print(f"{index}. {url}\tFetched in : {time.time() - start_time:.2f} seconds")
            extract_emails_from_text(page_content, email_file)
    except urllib.error.HTTPError as err:
        handle_http_error(url, err, email_file, index)
    except urllib.error.URLError as err:
        print(f"URLError for {url}: {err}")
    except Exception as e:
        print(f"An error occurred with {url}: {e}")

# Handle HTTP errors
def handle_http_error(url, error, email_file, index):
    print(f"HTTPError for {url}: {error}")
    if error.code == 404:
        cached_url = f'http://webcache.googleusercontent.com/search?q=cache:{url}'
        print(f"Trying cached version for {url}")
        try:
            fetch_html_content(cached_url, email_file, index)
        except Exception as e:
            print(f"Failed to fetch cached version for {url}: {e}")

# Main function
def main():
    start_time = time.time()
    url_found = False
    
    with open("urls.txt", 'r') as url_file, open("emails.txt", 'a') as email_file:
        for i, url_link in enumerate(url_file, start=1):
            url_link = url_link.strip().strip('\'"')
            
            # Skip empty lines and lines starting with "#"
            if not url_link or url_link.startswith("#"):
                continue
            
            # Add http prefix if missing
            if not url_link.startswith("http"):
                url_link = "http://" + url_link
            
            fetch_html_content(url_link, email_file, i)

    if not url_found:
        print("No Valid URLs found in the urls.txt file")
    else:
        print(f"Elapsed Time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
