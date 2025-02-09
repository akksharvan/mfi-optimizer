import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split

class InterestRateModel:
    def __init__(self):
        self.pipeline = None
        self.features = [
            'loan_amount', 'business_type', 
            'location', 'season', 
            'repayment_history', 'existing_debt_ratio'
        ]
        self.target = 'default_prob'
        
    def preprocess(self, df):
        df['loan_size_category'] = pd.cut(
            df['loan_amount'],
            bins=[0, 200, 500, 1000, 2000],
            labels=['micro', 'small', 'medium', 'large']
        )
        return df

    def build_pipeline(self):
        numeric_features = ['loan_amount', 'repayment_history', 'existing_debt_ratio']
        categorical_features = ['business_type', 'location', 'season']
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ]
        )
        
        return Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', HistGradientBoostingRegressor(
                max_iter=200,
                categorical_features=[3, 4, 5]
            ))
        ])

    def train(self, data_path):
        df = pd.read_csv(data_path)
        df = self.preprocess(df)
        
        X = df[self.features]
        y = df[self.target]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.pipeline = self.build_pipeline()
        self.pipeline.fit(X_train, y_train)
        
        train_score = self.pipeline.score(X_train, y_train)
        test_score = self.pipeline.score(X_test, y_test)
        print(f"Training R²: {train_score:.3f}, Test R²: {test_score:.3f}")
        
    def predict(self, input_data):
        df = pd.DataFrame([input_data])
        df = self.preprocess(df)
        return self.pipeline.predict(df)[0]