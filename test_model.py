import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.models.traffic_predictor import train_and_predict
import pandas as pd
import numpy as np

print("创建测试数据...")
features = pd.DataFrame({
    'flow': np.random.rand(200)*1000, 
    'speed': np.random.rand(200)*60, 
    'congestion_index': np.random.rand(200)
})
features['timestamp'] = pd.date_range('2024-01-01', periods=200, freq='h')

print("调用train_and_predict函数...")
result = train_and_predict(features)

print("测试成功!")
print(f"LSTM MAE: {result['lstm']['metrics']['MAE']:.2f}")
print(f"Prophet MAE: {result['prophet']['metrics']['MAE']:.2f}")