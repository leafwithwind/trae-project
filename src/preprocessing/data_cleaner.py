import pandas as pd
import numpy as np
from src.crawler.static_crawler import crawl_weather_data

def clean_data(static_data, dynamic_data):
    """
    清洗交通数据，处理缺失值和异常值
    """
    print("开始数据清洗...")
    
    # 合并静态数据和动态数据
    dynamic_df = dynamic_data.copy()
    
    # 1. 处理缺失值
    print("处理缺失值...")
    # 模拟数据中可能没有缺失值，这里添加一些缺失值进行演示
    # 随机设置一些缺失值
    np.random.seed(42)
    mask = np.random.rand(len(dynamic_df)) < 0.05
    dynamic_df.loc[mask, 'speed'] = np.nan
    mask = np.random.rand(len(dynamic_df)) < 0.03
    dynamic_df.loc[mask, 'flow'] = np.nan
    
    # 使用前向填充和后向填充处理缺失值
    dynamic_df['speed'] = dynamic_df['speed'].ffill().bfill()
    dynamic_df['flow'] = dynamic_df['flow'].ffill().bfill()
    
    # 2. 处理异常值
    print("处理异常值...")
    # 使用IQR方法检测异常值
    for col in ['speed', 'flow', 'congestion_index']:
        Q1 = dynamic_df[col].quantile(0.25)
        Q3 = dynamic_df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # 替换异常值为上下界
        dynamic_df[col] = dynamic_df[col].clip(lower=lower_bound, upper=upper_bound)
    
    # 3. 时序对齐
    print("时序对齐...")
    # 确保时间戳是正确的时间格式
    dynamic_df['timestamp'] = pd.to_datetime(dynamic_df['timestamp'])
    dynamic_df = dynamic_df.sort_values('timestamp')
    
    print("数据清洗完成")
    return dynamic_df

def feature_engineering(data):
    """
    特征工程，提取时间特征和其他相关特征
    """
    print("开始特征工程...")
    
    # 复制数据
    features = data.copy()
    
    # 1. 提取时间特征
    features['hour'] = features['timestamp'].dt.hour
    features['day_of_week'] = features['timestamp'].dt.dayofweek
    features['month'] = features['timestamp'].dt.month
    features['is_weekend'] = features['day_of_week'].isin([5, 6]).astype(int)
    features['is_peak_hour'] = ((features['hour'] >= 7) & (features['hour'] <= 9)) | ((features['hour'] >= 17) & (features['hour'] <= 19)).astype(int)
    
    # 2. 添加天气数据
    weather_data = crawl_weather_data()
    # 按日期合并天气数据
    features['date'] = features['timestamp'].dt.date
    weather_data['date'] = weather_data['date'].dt.date
    features = features.merge(weather_data, on='date', how='left')
    
    # 3. 计算衍生特征
    features['speed_flow_ratio'] = features['speed'] / (features['flow'] + 1)  # 避免除零
    features['congestion_level'] = pd.cut(features['congestion_index'], 
                                         bins=[0, 0.3, 0.6, 0.8, 1.0], 
                                         labels=[0, 1, 2, 3], 
                                         right=False).astype('Int64')
    
    # 4. 选择特征列
    feature_columns = ['hour', 'day_of_week', 'month', 'is_weekend', 'is_peak_hour',
                      'temperature', 'humidity', 'precipitation', 'wind_speed',
                      'speed', 'flow', 'congestion_index', 'speed_flow_ratio']
    
    features = features[feature_columns]
    
    print("特征工程完成")
    return features