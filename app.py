from fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd
from io import BytesIO

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        raise HTTPException(status_code=400, detail="Invalid file type")

    try:
        contents = await file.read()
        data = pd.read_excel(BytesIO(contents), engine='openpyxl')

        if 'Input' not in data.columns:
            raise HTTPException(status_code=400, detail="Column Input not found in the input file")

        data = calculate_columns(data)
        data.to_csv("output.csv", index=False)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"filename": file.filename}


def calculate_columns(df):
    df['Change'] = df['Input'].diff()
    df['Gain'] = df['Change'].apply(lambda x: x if x > 0 else 0)
    df['Loss'] = df['Change'].apply(lambda x: -x if x < 0 else 0)

    # Calculate initial Avg Gain and Avg Loss for the first 14-day period
    df['Avg Gain'] = 0.0
    df['Avg Loss'] = 0.0

    df.loc[15, 'Avg Gain'] = df['Gain'].iloc[2:16].sum() / 14
    df.loc[15, 'Avg Loss'] = df['Loss'].iloc[2:16].sum() / 14

    # Calculate subsequent Avg Gain and Avg Loss
    for i in range(16, len(df)):
        df.loc[i, 'Avg Gain'] = ((df.loc[i-1, 'Avg Gain'] * 13) + df.loc[i, 'Gain']) / 14
        df.loc[i, 'Avg Loss'] = ((df.loc[i-1, 'Avg Loss'] * 13) + df.loc[i, 'Loss']) / 14

    df['HM'] = df['Avg Gain'] / df['Avg Loss']
    df['14-day HMA'] = df.apply(lambda row: 0 if row['Avg Loss'] == 0 else 100 - (100 / (1 + row['HM'])), axis=1)

    # Reorder columns
    df = df[['Input', 'Change', 'Gain', 'Loss', 'Avg Gain', 'Avg Loss', 'HM', '14-day HMA']]

    return df


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
