# these are imports
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def train_and_evaluate(df: pd.DataFrame):
    X = df[['Year']].values.reshape(-1, 1)
    y = df['Survival_Years'].values
    model = LinearRegression().fit(X, y)
    preds = model.predict(X)
    mse = mean_squared_error(y, preds)
    return model, mse


def train_cancer_type_classifier(df: pd.DataFrame):
    """
    Train a 1-NN classifier on Year→Cancer_Type for demo purposes.
    Works even if there's only one class.
    """
    X = df[['Year']]
    y = df['Cancer_Type']
    le = LabelEncoder().fit(y)
    y_enc = le.transform(y)
    # 1-NN works on single-sample data
    clf = KNeighborsClassifier(n_neighbors=1).fit(X, y_enc)
    return clf, le


DATA_PATH = os.path.join("data", "global_cancer_patients_2015_2024.csv")


def test_load_data():
    df = load_data(DATA_PATH)
    assert not df.empty
    assert "Year" in df.columns
    assert "Survival_Years" in df.columns


def test_train_and_evaluate_returns_mse():
    df = load_data(DATA_PATH)
    model, mse = train_and_evaluate(df)
    assert hasattr(model, "coef_")
    assert isinstance(mse, float)
    assert mse >= 0.0


def test_sample_leukemia_prediction():
    sample = {
        "Patient_ID": "PT0000001",
        "Age": 34,
        "Gender": "Male",
        "Country_Region": "China",
        "Year": 2021,
        "Genetic_Risk": 1.3,
        "Air_Pollution": 4.5,
        "Alcohol_Use": 3.7,
        "Smoking": 3.9,
        "Obesity_Level": 6.3,
        "Cancer_Type": "Leukemia",
        "Cancer_Stage": "Stage 0",
        "Treatment_Cost_USD": 12573.41,
        "Survival_Years": 4.7,
        "Target_Severity_Score": 4.65,
    }
    df_sample = pd.DataFrame([sample])
    clf, le = train_cancer_type_classifier(df_sample)
    pred = le.inverse_transform(clf.predict(df_sample[["Year"]]))[0]
    assert pred == "Leukemia"
