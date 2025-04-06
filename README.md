# Wallet Management and Monetization System for WSO2

This project implements a wallet management system that integrates with ZarinPal for wallet top-ups and WSO2 API Manager for monetizing API calls by deducting a fixed cost from the user's wallet per call. It provides a seamless way to manage wallet balances and enforce payment for API usage.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Flask Application Setup](#flask-application-setup)
  - [WSO2 API Manager Setup](#wso2-api-manager-setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Wallet Management and Monetization System combines two core components:

1. **Flask Application**: Manages wallet balances, integrates with ZarinPal for secure payment processing, and exposes an endpoint for WSO2 API Manager to deduct funds based on API usage.
2. **WSO2 API Manager**: Tracks API calls and uses a custom handler to deduct a predefined cost from the user's wallet for each call.

This system ensures users maintain sufficient wallet balances to access APIs, providing an effective monetization framework.

## Features

- **Wallet Top-Up**: Securely add funds to the wallet via ZarinPal.
- **API Call Monetization**: Automatically deducts a fixed amount from the wallet per API call.
- **Balance Inquiry**: Check the current wallet balance at any time.
- **Database Support**: Uses SQLite by default (easily adaptable to other databases like MySQL).
- **Secure Payments**: Leverages ZarinPal for reliable and secure transactions.

## Project Structure

```
wallet_project/
├── app/
│   ├── __init__.py       # Initializes Flask app and database
│   ├── models.py         # Defines the Wallet model
│   ├── routes.py         # Contains Flask routes for wallet management
│   ├── config.py         # Configuration settings (e.g., secret key)
│   └── zarinpal.py       # ZarinPal payment integration logic
├── instance/
│   └── wallet.db         # SQLite database file
├── requirements.txt      # Python dependencies
└── run.py                # Entry point to launch the Flask app
```

## Prerequisites

Before setting up the project, ensure you have the following:

- **Python 3.6+**: Required to run the Flask application.
- **Flask and Dependencies**: Installed via `requirements.txt`.
- **WSO2 API Manager**: Version 4.2.0 or higher.
- **MySQL**: Optional for WSO2 API Manager in production (SQLite used by default for Flask).
- **ZarinPal Account**: Needed for payment processing; obtain a merchant ID.

## Setup Instructions

### Flask Application Setup



1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the Application**:
   - Open `app/config.py` and set a secure `SECRET_KEY`.
   - In `app/routes.py`, replace `your_merchant_id` with your ZarinPal merchant ID.

3. **Run the Application**:
   ```bash
   python run.py
   ```
   - The Flask app will start at `http://localhost:5000`.

### WSO2 API Manager Setup

1. **Install WSO2 API Manager**:
   - Download and install it following the [official guide](https://apim.docs.wso2.com/en/latest/install-and-setup/installation-guide/).

2. **Set Up MySQL Database** (Optional):
   - Use a bash script like this to configure MySQL for WSO2:
     ```bash
     ./setup_mysql_for_wso2.sh
     ```
   - Update the script with your MySQL credentials and WSO2 installation path.

3. **Start WSO2 API Manager**:
   - Run it with a script like:
     ```bash
     ./run_wso2.sh
     ```
   - Set the `API_M_HOME` variable to your WSO2 API Manager directory.

4. **Add Custom Handler**:
   - Write a custom handler in WSO2 to call the Flask `/deduct` endpoint for each API call.
   - See the [WSO2 documentation](https://apim.docs.wso2.com/en/latest/develop/extending-api-manager/writing-custom-handlers/) for guidance.

## Usage

1. **Top-Up Wallet**:
   - Visit `http://localhost:5000/topup`.
   - Enter an amount and submit to start the ZarinPal payment process.

2. **Check Wallet Balance**:
   - Go to `http://localhost:5000/balance` to view your current balance.

3. **API Call Deduction**:
   - Each API call via WSO2 API Manager triggers the custom handler, which calls `/deduct` to reduce the wallet balance.

## API Endpoints

- **`/topup` [GET, POST]**:
  - **GET**: Shows a form to input the top-up amount.
  - **POST**: Initiates payment with ZarinPal.

- **`/callback` [GET]**:
  - Processes the ZarinPal payment callback to update the wallet balance.

- **`/deduct` [POST]**:
  - Deducts a fixed cost from the wallet.
  - **Request Body**: `{ "user_id": "string" }`.

- **`/balance` [GET]**:
  - Returns the user's current wallet balance.

## Contributing

We welcome contributions! To get started:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add new feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

