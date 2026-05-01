import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

def cluster_traffic_states(features):
    """
    对交通状态进行聚类分析
    """
    print("开始交通状态聚类分析...")
    
    # 选择用于聚类的特征
    cluster_features = features[['speed', 'flow', 'congestion_index', 'speed_flow_ratio']]
    
    # 数据标准化
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(cluster_features)
    
    # 使用肘部法则确定最佳聚类数
    print("确定最佳聚类数...")
    inertia = []
    silhouette_scores = []
    k_range = range(2, 10)
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(scaled_features)
        inertia.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(scaled_features, kmeans.labels_))
    
    # 选择最佳聚类数（最大轮廓系数）
    best_k = k_range[np.argmax(silhouette_scores)]
    print(f"最佳聚类数: {best_k}")
    
    # 使用最佳聚类数进行聚类
    print(f"使用K={best_k}进行聚类...")
    kmeans = KMeans(n_clusters=best_k, random_state=42)
    clusters = kmeans.fit_predict(scaled_features)
    
    # 分析每个聚类的特征
    cluster_analysis = []
    for i in range(best_k):
        cluster_data = features[clusters == i]
        cluster_info = {
            'cluster_id': i,
            'size': len(cluster_data),
            'avg_speed': cluster_data['speed'].mean(),
            'avg_flow': cluster_data['flow'].mean(),
            'avg_congestion': cluster_data['congestion_index'].mean(),
            'avg_speed_flow_ratio': cluster_data['speed_flow_ratio'].mean()
        }
        cluster_analysis.append(cluster_info)
    
    cluster_df = pd.DataFrame(cluster_analysis)
    print("聚类分析结果:")
    print(cluster_df)
    
    # 为每个聚类分配交通状态标签
    # 根据拥堵指数和流量对聚类进行排序
    cluster_df = cluster_df.sort_values('avg_congestion', ascending=False)
    
    # 分配状态标签
    state_labels = ['严重拥堵', '中度拥堵', '轻度拥堵', '畅通']
    if best_k <= len(state_labels):
        cluster_df['state'] = state_labels[:best_k]
    else:
        # 如果聚类数超过预设标签数，使用通用标签
        cluster_df['state'] = [f'状态{i}' for i in range(best_k)]
    
    # 创建聚类结果映射
    cluster_map = dict(zip(cluster_df['cluster_id'], cluster_df['state']))
    features['cluster'] = clusters
    features['traffic_state'] = features['cluster'].map(cluster_map)
    
    print("交通状态聚类完成")
    return {
        'clusters': clusters,
        'cluster_analysis': cluster_df,
        'labeled_data': features
    }