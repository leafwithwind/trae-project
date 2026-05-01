import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from src.crawler import static_crawler, dynamic_crawler
from src.preprocessing import data_cleaner
from src.models import traffic_predictor
from src.clustering import traffic_cluster

def run_experiment():
    """
    运行完整的实验并生成报告
    """
    print("=== 开始实验 ===")
    
    # 1. 数据采集
    print("\n1. 数据采集")
    static_data = static_crawler.crawl_static_data()
    dynamic_data = dynamic_crawler.crawl_dynamic_data()
    weather_data = static_crawler.crawl_weather_data()
    
    print(f"静态数据: 道路段数={len(static_data['road_sections'])}, 监测点数={len(static_data['monitoring_points'])}")
    print(f"动态数据: 数据点数量={len(dynamic_data)}")
    print(f"天气数据: 天数={len(weather_data)}")
    
    # 2. 数据清洗和特征工程
    print("\n2. 数据清洗和特征工程")
    cleaned_data = data_cleaner.clean_data(static_data, dynamic_data)
    features = data_cleaner.feature_engineering(cleaned_data)
    
    print(f"清洗后数据: 行数={len(cleaned_data)}")
    print(f"特征工程后: 特征数={len(features.columns)}")
    
    # 3. 模型训练和预测
    print("\n3. 模型训练和预测")
    predictions = traffic_predictor.train_and_predict(features)
    
    # 4. 交通状态聚类
    print("\n4. 交通状态聚类")
    clusters = traffic_cluster.cluster_traffic_states(features)
    
    # 5. 生成实验报告
    print("\n5. 生成实验报告")
    generate_report(predictions, clusters, features)
    
    print("\n=== 实验完成 ===")

def generate_report(predictions, clusters, features):
    """
    生成实验报告
    """
    # 创建报告目录
    import os
    os.makedirs('reports', exist_ok=True)
    
    # 1. 模型评估报告
    print("生成模型评估报告...")
    model_report = {
        'lstm_metrics': predictions['lstm']['metrics'],
        'prophet_metrics': predictions['prophet']['metrics']
    }
    
    with open('reports/model_evaluation.json', 'w', encoding='utf-8') as f:
        json.dump(model_report, f, ensure_ascii=False, indent=2)
    
    # 2. 聚类分析报告
    print("生成聚类分析报告...")
    cluster_report = clusters['cluster_analysis'].to_dict('records')
    
    with open('reports/cluster_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(cluster_report, f, ensure_ascii=False, indent=2)
    
    # 3. 数据统计报告
    print("生成数据统计报告...")
    data_stats = features.describe().to_dict()
    
    with open('reports/data_statistics.json', 'w', encoding='utf-8') as f:
        json.dump(data_stats, f, ensure_ascii=False, indent=2)
    
    # 4. 生成可视化图表
    print("生成可视化图表...")
    generate_visualizations(predictions, clusters, features)
    
    # 5. 生成综合报告
    print("生成综合报告...")
    with open('reports/experiment_report.md', 'w', encoding='utf-8') as f:
        f.write("# 智慧交通数据分析系统实验报告\n\n")
        f.write("## 1. 实验概述\n")
        f.write("本实验实现了一套完整的交通数据爬取、流量预测与智慧交通分析模型系统，包括数据采集、清洗、特征工程、模型训练、预测和可视化等功能。\n\n")
        
        f.write("## 2. 数据情况\n")
        f.write(f"- 静态数据: 道路段数={len(static_crawler.crawl_static_data()['road_sections'])}, 监测点数={len(static_crawler.crawl_static_data()['monitoring_points'])}\n")
        f.write(f"- 动态数据: 数据点数量={len(dynamic_crawler.crawl_dynamic_data())}\n")
        f.write(f"- 天气数据: 天数={len(static_crawler.crawl_weather_data())}\n\n")
        
        f.write("## 3. 模型评估\n")
        f.write("### LSTM模型\n")
        f.write(f"- MAE: {predictions['lstm']['metrics']['MAE']:.2f}\n")
        f.write(f"- MSE: {predictions['lstm']['metrics']['MSE']:.2f}\n")
        f.write(f"- RMSE: {predictions['lstm']['metrics']['RMSE']:.2f}\n\n")
        
        f.write("### Prophet模型\n")
        f.write(f"- MAE: {predictions['prophet']['metrics']['MAE']:.2f}\n")
        f.write(f"- MSE: {predictions['prophet']['metrics']['MSE']:.2f}\n")
        f.write(f"- RMSE: {predictions['prophet']['metrics']['RMSE']:.2f}\n\n")
        
        f.write("## 4. 交通状态聚类\n")
        f.write("### 聚类结果\n")
        for i, row in clusters['cluster_analysis'].iterrows():
            f.write(f"- 聚类{i}: 大小={row['size']}, 平均速度={row['avg_speed']:.2f}, 平均流量={row['avg_flow']:.2f}, 平均拥堵指数={row['avg_congestion']:.2f}, 状态={row['state']}\n")
        f.write("\n")
        
        f.write("## 5. 结论与建议\n")
        f.write("### 结论\n")
        f.write("1. 本系统成功实现了交通数据的采集、清洗、分析和预测功能\n")
        f.write("2. LSTM模型在交通流量预测方面表现较好，能够捕捉时间序列的长期依赖关系\n")
        f.write("3. 交通状态聚类分析能够有效识别不同拥堵程度的交通状态\n")
        f.write("4. 可视化平台提供了直观的数据展示和分析工具\n\n")
        
        f.write("### 改进建议\n")
        f.write("1. 增加更多的数据源，如GPS数据、摄像头数据等\n")
        f.write("2. 优化模型参数，提高预测精度\n")
        f.write("3. 增加实时数据更新和预警功能\n")
        f.write("4. 扩展可视化平台的功能，增加更多交互元素\n")
        f.write("5. 考虑使用更先进的深度学习模型，如Transformer等\n")

def generate_visualizations(predictions, clusters, features):
    """
    生成可视化图表
    """
    import os
    os.makedirs('reports/figures', exist_ok=True)
    
    # 1. 模型预测对比图
    plt.figure(figsize=(12, 6))
    plt.plot(predictions['lstm']['y_true'][:50], label='真实值')
    plt.plot(predictions['lstm']['y_pred'][:50], label='LSTM预测值')
    plt.plot(predictions['prophet']['y_pred'][:50], label='Prophet预测值')
    plt.title('模型预测对比')
    plt.xlabel('时间')
    plt.ylabel('流量')
    plt.legend()
    plt.savefig('reports/figures/prediction_comparison.png')
    plt.close()
    
    # 2. 模型评估指标对比
    metrics = pd.DataFrame({
        '指标': ['MAE', 'MSE', 'RMSE'],
        'LSTM': [
            predictions['lstm']['metrics']['MAE'],
            predictions['lstm']['metrics']['MSE'],
            predictions['lstm']['metrics']['RMSE']
        ],
        'Prophet': [
            predictions['prophet']['metrics']['MAE'],
            predictions['prophet']['metrics']['MSE'],
            predictions['prophet']['metrics']['RMSE']
        ]
    })
    
    plt.figure(figsize=(10, 6))
    metrics.set_index('指标').plot(kind='bar')
    plt.title('模型评估指标对比')
    plt.ylabel('值')
    plt.tight_layout()
    plt.savefig('reports/figures/metrics_comparison.png')
    plt.close()
    
    # 3. 交通状态分布
    plt.figure(figsize=(10, 6))
    state_counts = clusters['labeled_data']['traffic_state'].value_counts()
    state_counts.plot(kind='bar')
    plt.title('交通状态分布')
    plt.xlabel('交通状态')
    plt.ylabel('数量')
    plt.savefig('reports/figures/traffic_state_distribution.png')
    plt.close()
    
    # 4. 速度与流量关系散点图
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        clusters['labeled_data']['speed'],
        clusters['labeled_data']['flow'],
        c=clusters['labeled_data']['cluster'],
        cmap='viridis',
        alpha=0.6
    )
    plt.title('速度与流量关系（按交通状态聚类）')
    plt.xlabel('速度 (km/h)')
    plt.ylabel('流量')
    cbar = plt.colorbar(scatter)
    cbar.set_label('聚类')
    plt.savefig('reports/figures/speed_flow_scatter.png')
    plt.close()
    
    # 5. 拥堵指数时间序列
    plt.figure(figsize=(12, 6))
    plt.plot(features.index[:100], features['congestion_index'][:100])
    plt.title('拥堵指数时间序列')
    plt.xlabel('时间')
    plt.ylabel('拥堵指数')
    plt.savefig('reports/figures/congestion_time_series.png')
    plt.close()

if __name__ == "__main__":
    run_experiment()