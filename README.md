# Excel File Processor API

This is a FastAPI-based application that processes an uploaded Excel file to calculate various columns based on the values in the 'Input' column. The resulting data is then saved as a CSV file.

## Features

- Upload an Excel file (`.xlsx`)
- Validate the file type and content
- Calculate specific columns based on the 'Input' column
- Save the processed data to an output CSV file

## Endpoints

### POST /uploadfile/

#### Request

- **File**: An Excel file (`.xlsx`) with an 'Input' column.

#### Response

- **Filename**: The name of the uploaded file.

## Calculation Logic

The application calculates the following columns based on the 'Input' column:

- `Change`: The difference between the current and previous input values.
- `Gain`: The positive changes (if any), otherwise zero.
- `Loss`: The negative changes (if any), otherwise zero.
- `Avg Gain`: The average gain over a 14-day period.
- `Avg Loss`: The average loss over a 14-day period.
- `HM`: The ratio of the average gain to the average loss.
- `14-day HMA`: The 14-day HMA value based on the calculated HM.

## Running the Application

To run the application, use the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
Replace main with the name of your Python file if different.

## Example Usage
You can test the API using a tool like curl or Postman.

## Using curl
```bash
curl -X POST "http://127.0.0.1:8000/uploadfile/" -F "file=@/path/to/yourfile.xlsx"
```

## Using Postman
Create a new POST request.
Set the URL to `http://127.0.0.1:8000/uploadfile/`.
In the body section, select form-data.
Add a key named file, select File as the type, and choose your Excel file.

## Dependencies
FastAPI
pandas
openpyxl
uvicorn

## Installation
- **Clone the repository**:
```bash
git clone https://github.com/osamayy515/excel_calculator.git
```
- **Navigate to the project directory**:
```bash
cd your-repo-name
```
- **Install the required packages**:
```bash
pip install -r requirements.txt
```
