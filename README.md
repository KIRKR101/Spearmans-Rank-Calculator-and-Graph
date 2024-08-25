# Spearman's Rank Correlation Coefficient Calculator
Simple PyQt5 GUI to calculate Spearman's rank correlation coefficient.

This is a Python application with a GUI that calculates Spearman's Rank Correlation Coefficient (SRCC). It allows users to input data manually or import data from a CSV file. The application provides the correlation coefficient, the type of correlation, and the strength of the correlation. The result can be exported as PNG or CSV.

$$
\rho = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)}
$$

Where:
- \( \rho \) is the Spearman's Rank Correlation Coefficient.
- \( d_i \) is the difference between the ranks of corresponding values.
- \( n \) is the number of observations.

## Features
- Ability to: Input data manually in various number formats or import data from CSV files, like the example `spearmans-correlation-data.csv`
- Display correlation type (Positive, Negative, or No correlation) and correlation strength (Weak, Moderate, or Strong) 
- Generates a scatter plot of the data, and the ability to export it as a PNG, like example `sample.png`
- ![sample](https://github.com/user-attachments/assets/3b54b33c-127e-4f59-88df-a8033664f6c7)
- Export the results (X and Y values, correlation coefficient) as a CSV file, like [CSVexportsample.csv](https://github.com/user-attachments/files/16740118/CSVexportsample.csv)
- Modern, responsive GUI using PyQt5
## Usage
- Clone the repository / download the python script by itself
- Install dependencies: `PyQt5`, `matplotlib`: ``pip install PyQt5 matplotlib numpy`` (`re`, `csv` and `sys` are part of Python's standard library)
- Run the script with: `python srcc.py`
