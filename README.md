# Insighta CLI

A powerful command-line interface for managing and querying user profiles with integrated GitHub OAuth authentication.

## Overview

Insighta CLI is a Python-based tool that provides seamless access to profile data through an intuitive command-line interface. It features GitHub OAuth authentication, advanced profile searching, filtering, and export capabilities.

## Features

- **GitHub OAuth Authentication**: Secure login via GitHub using PKCE flow
- **Profile Management**: List, search, create, and retrieve detailed profile information
- **Advanced Filtering**: Filter profiles by gender, country, age group, and age range
- **Sorting**: Sort results by various fields (age, creation date, etc.)
- **Pagination**: Navigate through large result sets with customizable page sizes
- **Display Options**: Beautiful terminal output with formatted tables using Rich
- **Export Functionality**: Export profile data in various formats
- **Natural Language Search**: Semantic profile search capabilities

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd insighta_cli
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the package:

```bash
pip install -e .
```

Or install dependencies manually:

```bash
pip install -r requirements.txt
```

## Quick Start

### Authentication

First, authenticate with your GitHub account:

```bash
insighta login
```

This will open your browser for GitHub authentication. Once authorized, your tokens will be saved securely.

### List Profiles

```bash
# List all profiles (default: 10 per page)
insighta profiles list

# With pagination
insighta profiles list --page 2 --limit 20

# Filter by gender and country
insighta profiles list --gender male --country NG

# Filter by age range
insighta profiles list --min-age 18 --max-age 35

# Sort results
insighta profiles list --sort-by age --order desc
```

### Search Profiles

Search for profiles using natural language queries:

```bash
insighta profiles search "young professionals in Nigeria"
```

### Get Profile Details

Retrieve detailed information for a specific profile:

```bash
insighta profiles get <profile-id>
```

### Create a Profile

Generate a new profile based on a name:

```bash
insighta profiles create --name "John Doe"
```

### Export Profiles

Export profile data to a file:

```bash
insighta profiles export <output-file>
```

## Command Reference

### `insighta auth`

Authentication commands for managing your session.

#### `auth login`

Authenticate with GitHub using OAuth 2.0 with PKCE flow.

**Usage:**

```bash
insighta auth login
```

### `insighta profiles`

Profile management and querying commands.

#### `profiles list`

List profiles with advanced filtering and sorting options.

**Options:**

- `--gender TEXT`: Filter by gender (male/female)
- `--country TEXT`: Filter by country ID (e.g., US, NG)
- `--age-group TEXT`: Filter by age group
- `--min-age INTEGER`: Minimum age limit
- `--max-age INTEGER`: Maximum age limit
- `--sort-by TEXT`: Field to sort by (age, created_at)
- `--order TEXT`: Sort order (asc/desc)
- `--page INTEGER`: Page number (default: 1)
- `--limit INTEGER`: Items per page (default: 10)

#### `profiles search`

Search profiles using natural language queries.

**Usage:**

```bash
insighta profiles search "your search query"
```

#### `profiles get`

Retrieve detailed information for a specific profile.

**Usage:**

```bash
insighta profiles get <profile-id>
```

#### `profiles create`

Create a new profile by providing a name.

**Options:**

- `--name TEXT`: Name of the person to generate a profile for (required)

**Usage:**

```bash
insighta profiles create --name "Jane Smith"
```

#### `profiles export`

Export profile data to a file.

**Usage:**

```bash
insighta profiles export output.csv
```

## Project Structure

```
insighta_cli/
├── insighta/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── api.py               # API request handling
│   ├── config.py            # Configuration settings
│   ├── storage.py           # Token persistence
│   └── commands/
│       ├── __init__.py
│       ├── auth.py          # Authentication commands
│       └── profiles.py      # Profile management commands
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Configuration

Configuration is managed through environment variables and saved tokens. The CLI uses:

- `BASE_URL`: Backend API base URL
- `CLI_BASE_URL`: CLI callback URL for OAuth redirect

Tokens are securely stored and automatically used for authenticated requests.

## Technical Stack

- **Typer**: Modern CLI framework for Python
- **Rich**: Beautiful terminal output formatting
- **Requests**: HTTP client for API calls
- **Python**: Core language

## Dependencies

See [requirements.txt](requirements.txt) for the complete list of dependencies.

## Authentication Flow

Insighta CLI uses GitHub OAuth with PKCE (Proof Key for Code Exchange) for secure authentication:

1. User initiates login command
2. Local HTTP callback server starts on port 9000
3. Browser opens for GitHub authentication
4. Authorization code is received via callback
5. Code is exchanged for access tokens with backend
6. Tokens are securely stored for future requests

## Error Handling

The CLI provides clear error messages and status feedback:

- **Login failures**: Display specific error messages from failed authentication
- **API errors**: Show relevant error details from API responses
- **Network issues**: Graceful handling with timeout mechanisms

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
