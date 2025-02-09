import pandas as pd
import numpy as np

def generate_mfi_data(num_samples=5000):
    np.random.seed(42)
    data = {
        'loan_amount': np.random.randint(50, 2000, num_samples),
        'business_type': np.random.choice(
            ['Agriculture', 'Retail', 'Handicraft', 'Livestock'], 
            num_samples,
            p=[0.4, 0.3, 0.2, 0.1]
        ),
        'location': np.random.choice(['Urban', 'Rural'], num_samples, p=[0.3, 0.7]),
        'season': np.random.choice(
            ['Planting', 'Harvest', 'Lean'], 
            num_samples,
            p=[0.3, 0.4, 0.3]
        ),
        'repayment_history': np.clip(np.random.beta(2, 5, num_samples) + 0.2, 0, 1),
        'existing_debt_ratio': np.random.uniform(0, 0.8, num_samples)
    }
    
    data['default_prob'] = (
        0.3 * (data['business_type'] == 'Agriculture') * 
        (data['season'] == 'Lean') +
        0.2 * data['existing_debt_ratio'] +
        0.15 * (1 - data['repayment_history']) +
        np.random.normal(0, 0.1, num_samples)
    )
    
    df = pd.DataFrame(data)
    df.to_csv('backend/data/mfi_dataset.csv', index=False)
    return df

if __name__ == "__main__":
    generate_mfi_data()