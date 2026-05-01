import os
import sys
from src.crawler import static_crawler, dynamic_crawler
from src.preprocessing import data_cleaner
from src.models import traffic_predictor
from src.clustering import traffic_cluster
from src.visualization import dashboard

def main():
    print("=== 智慧交通数据分析系统 ===")
    
    # 1. 数据爬取
    print("1. 开始数据爬取...")
    static_data = static_crawler.crawl_static_data()
    dynamic_data = dynamic_crawler.crawl_dynamic_data()
    
    # 2. 数据清洗
    print("2. 开始数据清洗...")
    cleaned_data = data_cleaner.clean_data(static_data, dynamic_data)
    
    # 3. 特征工程
    print("3. 开始特征工程...")
    features = data_cleaner.feature_engineering(cleaned_data)
    
    # 4. 模型训练和预测
    print("4. 开始模型训练和预测...")
    predictions = traffic_predictor.train_and_predict(features)
    
    # 5. 交通状态聚类
    print("5. 开始交通状态聚类...")
    clusters = traffic_cluster.cluster_traffic_states(features)
    
    # 6. 可视化展示
    print("6. 可视化展示准备完成...")
    print("请在终端执行以下命令启动可视化仪表盘:")
    print("streamlit run src/visualization/dashboard.py")

if __name__ == "__main__":
    main()