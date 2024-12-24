import pandas as pd
from datetime import datetime, timedelta

# Create sample data with correct status choices
data = {
    'company_name': ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple'],
    'job_title': ['Software Engineer', 'DevOps Engineer', 'Full Stack Developer', 'Data Scientist', 'iOS Developer'],
    # Using exact status values from the Application model
    'status': ['Pending', 'Interview', 'Offer', 'Rejected', 'Pending'],
    'date_applied': [
        (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') 
        for i in range(5)
    ],
    'job_description': [
        'Full stack role with focus on Python and React',
        'Cloud infrastructure and automation',
        'Building scalable web applications',
        'Machine learning and data analysis',
        'iOS app development using Swift'
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
df.to_excel('test_import.xlsx', index=False)
print("Created test_import.xlsx successfully!")
print("\nDataFrame Preview:")
print(df.head())