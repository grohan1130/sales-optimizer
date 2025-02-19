# Sales Price Optimizer

A Flask web application that helps determine optimal sales prices for new products based on historical sales data. The application calculates expected sales volumes and profits at different price points to find the most profitable selling price.

## Features

- Upload historical sales data in Excel (.xlsx, .xls) or CSV format
- Input cost and price parameters for new products
- View optimized price calculations and projected volumes
- See expected revenue and profit projections

## Installation

1. Clone the repository
2. Create a virtual environment:

```python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:

```python
pip install -r requirements.txt
```

## Usage

1. Run the application:

```python
python run.py
```

2. Access the application at: http://localhost:5001

3. Input required fields:
   - Unit Cost of Production ($)
   - Best-guess Viable Sales Price ($)
   - Maximum Viable Sales Price ($)
   - Upload historical sales data file

## Data File Format

Your Excel/CSV file should contain:

- First column: Product identifiers (e.g., XCR codes)
- Columns 2-13: Monthly sales volumes (January through December)

## Price-Volume Relationship

The application assumes:

- At best-guess price: 100% of historical average volume
- At maximum price: 0% volume
- Linear volume reduction between these points

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── file_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── file_service.py
│   │   └── optimization_service.py
│   └── templates/
│       ├── upload.html
│       └── result.html
├── config.py
├── run.py
├── requirements.txt
└── .gitignore
```

## Dependencies

- Flask
- Pandas
- NumPy
- openpyxl (for Excel file support)

## Input Validation

The application validates:

- All prices must be positive
- Cost must be less than best-guess price
- Best-guess price must be less than maximum price
- Minimum 5% profit margin requirement
