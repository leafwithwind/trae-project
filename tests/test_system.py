import pytest
import pandas as pd
import numpy as np
from src.crawler import static_crawler, dynamic_crawler
from src.preprocessing import data_cleaner
from src.models import traffic_predictor
from src.clustering import traffic_cluster

def test_static_crawler():
    """
    测试静态数据爬取模块
    """
    print("测试静态数据爬取模块...")
    static_data = static_crawler.crawl_static_data()
    assert 'road_sections' in static_data
    assert 'monitoring_points' in static_data
    assert not static_data['road_sections'].empty
    assert not static_data['monitoring_points'].empty
    print("静态数据爬取模块测试通过")

def test_dynamic_crawler():
    """
    测试动态数据爬取模块
    """
    print("测试动态数据爬取模块...")
    dynamic_data = dynamic_crawler.crawl_dynamic_data()
    assert not dynamic_data.empty
    assert 'point_id' in dynamic_data.columns
    assert 'timestamp' in dynamic_data.columns
    assert 'speed' in dynamic_data.columns
    assert 'flow' in dynamic_data.columns
    assert 'congestion_index' in dynamic_data.columns
    print("动态数据爬取模块测试通过")

def test_data_cleaner():
    """
    测试数据清洗模块
    """
    print("测试数据清洗模块...")
    # 准备测试数据
    static_data = static_crawler.crawl_static_data()
    dynamic_data = dynamic_crawler.crawl_dynamic_data()
    
    # 测试数据清洗
    cleaned_data = data_cleaner.clean_data(static_data, dynamic_data)
    assert not cleaned_data.empty
    assert cleaned_data['speed'].isna().sum() == 0
    assert cleaned_data['flow'].isna().sum() == 0
    assert cleaned_data['congestion_index'].isna().sum() == 0
    
    # 测试特征工程
    features = data_cleaner.feature_engineering(cleaned_data)
    assert not features.empty
    assert 'hour' in features.columns
    assert 'day_of_week' in features.columns
    assert 'temperature' in features.columns
    assert 'humidity' in features.columns
    print("数据清洗模块测试通过")

def test_traffic_predictor():
    """
    测试交通流量预测模块
    """
    print("测试交通流量预测模块...")
    # 准备测试数据
    static_data = static_crawler.crawl_static_data()
    dynamic_data = dynamic_crawler.crawl_dynamic_data()
    cleaned_data = data_cleaner.clean_data(static_data, dynamic_data)
    features = data_cleaner.feature_engineering(cleaned_data)
    
    # 测试预测模型
    predictions = traffic_predictor.train_and_predict(features)
    assert 'lstm' in predictions
    assert 'prophet' in predictions
    assert 'y_true' in predictions['lstm']
    assert 'y_pred' in predictions['lstm']
    assert 'metrics' in predictions['lstm']
    assert 'MAE' in predictions['lstm']['metrics']
    assert 'MSE' in predictions['lstm']['metrics']
    assert 'RMSE' in predictions['lstm']['metrics']
    print("交通流量预测模块测试通过")

def test_traffic_cluster():
    """
    测试交通状态聚类模块
    """
    print("测试交通状态聚类模块...")
    # 准备测试数据
    static_data = static_crawler.crawl_static_data()
    dynamic_data = dynamic_crawler.crawl_dynamic_data()
    cleaned_data = data_cleaner.clean_data(static_data, dynamic_data)
    features = data_cleaner.feature_engineering(cleaned_data)
    
    # 测试聚类分析
    clusters = traffic_cluster.cluster_traffic_states(features)
    assert 'clusters' in clusters
    assert 'cluster_analysis' in clusters
    assert 'labeled_data' in clusters
    assert not clusters['cluster_analysis'].empty
    assert 'traffic_state' in clusters['labeled_data'].columns
    print("交通状态聚类模块测试通过")

def test_integration():
    """
    测试系统集成
    """
    print("测试系统集成...")
    # 完整的系统流程测试
    static_data = static_crawler.crawl_static_data()
    dynamic_data = dynamic_crawler.crawl_dynamic_data()
    cleaned_data = data_cleaner.clean_data(static_data, dynamic_data)
    features = data_cleaner.feature_engineering(cleaned_data)
    predictions = traffic_predictor.train_and_predict(features)
    clusters = traffic_cluster.cluster_traffic_states(features)
    
    # 验证所有模块都正常工作
    assert static_data is not None
    assert dynamic_data is not None
    assert cleaned_data is not None
    assert features is not None
    assert predictions is not None
    assert clusters is not None
    print("系统集成测试通过")

if __name__ == "__main__":
    # 运行所有测试
    test_static_crawler()
    test_dynamic_crawler()
    test_data_cleaner()
    test_traffic_predictor()
    test_traffic_cluster()
    test_integration()
    print("所有测试通过！")