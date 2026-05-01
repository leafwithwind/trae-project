import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from src.crawler import static_crawler, dynamic_crawler
from src.preprocessing import data_cleaner
from src.models import traffic_predictor
from src.clustering import traffic_cluster

# 设置Matplotlib支持中文
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 获取真实数据
def get_real_data():
    """
    从爬虫获取真实的交通数据
    """
    # 爬取静态数据
    static_data = static_crawler.crawl_static_data()
    
    # 爬取动态数据
    dynamic_data = dynamic_crawler.crawl_dynamic_data()
    
    # 数据清洗
    cleaned_data = data_cleaner.clean_data(static_data, dynamic_data)
    
    # 特征工程
    features = data_cleaner.feature_engineering(cleaned_data)
    
    # 模型预测
    predictions = traffic_predictor.train_and_predict(features)
    
    # 交通状态聚类
    clusters = traffic_cluster.cluster_traffic_states(features)
    
    return features, predictions, clusters

# 主函数
def main():
    """
    运行交通数据可视化仪表盘
    """
    # 获取真实数据
    features, predictions, clusters = get_real_data()
    
    # 创建Streamlit应用
    st.title("智慧交通数据分析系统")
    
    # 侧边栏导航
    st.sidebar.title("导航")
    page = st.sidebar.radio("选择页面", ["数据概览", "流量预测", "交通状态分析", "模型评估"])
    
    if page == "数据概览":
        st.header("交通数据概览")
        
        # 数据统计信息
        st.subheader("数据统计")
        st.write(features.describe())
        
        # 速度和流量的时间序列图
        st.subheader("交通流量和速度趋势")
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))
        
        # 流量趋势
        axes[0].plot(features.index[:100], features['flow'][:100])
        axes[0].set_title('交通流量趋势')
        axes[0].set_xlabel('时间')
        axes[0].set_ylabel('流量')
        
        # 速度趋势
        axes[1].plot(features.index[:100], features['speed'][:100])
        axes[1].set_title('平均车速趋势')
        axes[1].set_xlabel('时间')
        axes[1].set_ylabel('速度 (km/h)')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # 拥堵指数分布
        st.subheader("拥堵指数分布")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(features['congestion_index'], bins=20, ax=ax)
        ax.set_title('拥堵指数分布')
        ax.set_xlabel('拥堵指数')
        ax.set_ylabel('频率')
        st.pyplot(fig)
    
    elif page == "流量预测":
        st.header("交通流量预测")
        
        # 选择预测模型
        model = st.selectbox("选择预测模型", ["LSTM", "Prophet"])
        
        if model == "LSTM":
            st.subheader("LSTM模型预测结果")
            # 绘制预测结果
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(predictions['lstm']['y_true'][:50], label='真实值')
            ax.plot(predictions['lstm']['y_pred'][:50], label='预测值')
            ax.set_title('LSTM模型流量预测')
            ax.set_xlabel('时间')
            ax.set_ylabel('流量')
            ax.legend()
            st.pyplot(fig)
            
            # 显示模型评估指标
            st.subheader("模型评估指标")
            metrics = predictions['lstm']['metrics']
            st.write(f"MAE: {metrics['MAE']:.2f}")
            st.write(f"MSE: {metrics['MSE']:.2f}")
            st.write(f"RMSE: {metrics['RMSE']:.2f}")
        
        else:
            st.subheader("Prophet模型预测结果")
            # 绘制预测结果
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(predictions['prophet']['y_true'][:50], label='真实值')
            ax.plot(predictions['prophet']['y_pred'][:50], label='预测值')
            ax.set_title('Prophet模型流量预测')
            ax.set_xlabel('时间')
            ax.set_ylabel('流量')
            ax.legend()
            st.pyplot(fig)
            
            # 显示模型评估指标
            st.subheader("模型评估指标")
            metrics = predictions['prophet']['metrics']
            st.write(f"MAE: {metrics['MAE']:.2f}")
            st.write(f"MSE: {metrics['MSE']:.2f}")
            st.write(f"RMSE: {metrics['RMSE']:.2f}")
    
    elif page == "交通状态分析":
        st.header("交通状态分析")
        
        # 显示聚类分析结果
        st.subheader("交通状态聚类分析")
        st.write(clusters['cluster_analysis'])
        
        # 交通状态分布
        st.subheader("交通状态分布")
        state_counts = clusters['labeled_data']['traffic_state'].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        state_counts.plot(kind='bar', ax=ax)
        ax.set_title('交通状态分布')
        ax.set_xlabel('交通状态')
        ax.set_ylabel('数量')
        st.pyplot(fig)
        
        # 交通状态特征散点图
        st.subheader("交通状态特征分析")
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(
            clusters['labeled_data']['speed'],
            clusters['labeled_data']['flow'],
            c=clusters['labeled_data']['cluster'],
            cmap='viridis',
            alpha=0.6
        )
        ax.set_title('速度与流量关系（按交通状态聚类）')
        ax.set_xlabel('速度 (km/h)')
        ax.set_ylabel('流量')
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('聚类')
        st.pyplot(fig)
    
    elif page == "模型评估":
        st.header("模型评估")
        
        # 模型对比
        st.subheader("模型性能对比")
        
        # 创建评估指标对比表
        metrics_df = pd.DataFrame({
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
        
        st.write(metrics_df)
        
        # 绘制指标对比图
        fig, ax = plt.subplots(figsize=(12, 6))
        metrics_df.set_index('指标').plot(kind='bar', ax=ax)
        ax.set_title('模型性能对比')
        ax.set_ylabel('值')
        plt.tight_layout()
        st.pyplot(fig)
        
        # 模型优缺点分析
        st.subheader("模型优缺点分析")
        st.write("**LSTM模型：**")
        st.write("- 优点：能够捕捉时间序列的长期依赖关系，预测精度较高")
        st.write("- 缺点：训练时间长，需要大量数据，对超参数敏感")
        
        st.write("**Prophet模型：**")
        st.write("- 优点：易于使用，能够处理季节性和节假日效应")
        st.write("- 缺点：对于复杂的非线性关系捕捉能力较弱")

# 运行应用
if __name__ == "__main__":
    main()