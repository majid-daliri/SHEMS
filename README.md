# Smart Home Energy Management System (SHEMS)

## Overview
The Smart Home Energy Management System (SHEMS) is a Flask-based web application designed to help homeowners efficiently manage and understand their energy consumption, ultimately aiding in the reduction of electricity bills. This system integrates with various smart electrical devices such as air conditioners, washers, dryers, refrigerators, ovens, and lights, providing detailed insights into energy usage patterns.

## Features
- **Energy Usage Tracking:** Monitors energy consumption of connected smart devices.
- **Historical Data Analysis:** Stores and displays historical energy usage, allowing users to understand their consumption patterns.
- **Appliance-Specific Insights:** Breaks down energy usage by individual appliances and settings.
- **User-Friendly Dashboard:** Provides an intuitive interface for easy access to all features.

## Installation

To set up the SHEMS project on your local machine, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/majid-daliri/SHEMS.git
   
2. **Clone the Repository:**
   ```bash
   cd Smart-Home-Energy-Management-System

3. Install Required Packages:
    ```bash
   pip install -r requirements.txt

4. Initialize the Database:
    ```bash
   flask db upgrade

5. Run the Application:
    ```bash
   flask run

## Usage

After starting the application, navigate to `http://localhost:5000` in your web browser. You can then register an account and start integrating your smart home devices.

