"""
clustering_pca.py

Module 2: k-means clustering, hierarchical clustering (cosine distance),
and PCA on the cleaned exoplanet dataset.

Input: exoplanets_clean.csv (from clean_and_visualize.py)
Outputs: the clustering/PCA charts used on the Clustering and PCA tabs.

Usage:
    pip install pandas numpy scikit-learn scipy matplotlib
    python clustering_pca.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import pdist

os.makedirs("charts", exist_ok=True)

df = pd.read_csv("exoplanets_clean.csv")

# ================= DATA PREP =================
# Clustering and PCA need unlabeled numeric data only, so just the eight
# physical measurement columns are used here, with rows missing any of
# them dropped.
numeric_cols = ["pl_orbper", "pl_rade", "pl_bmasse", "pl_eqt",
                 "st_teff", "st_rad", "st_mass", "sy_dist"]
cluster_df = df.dropna(subset=numeric_cols).reset_index(drop=True)
print("Rows with complete numeric data:", len(cluster_df), "of", len(df))

# these columns span several orders of magnitude (orbital period especially),
# so log-transform first so no single feature dominates the distance purely
# because of its raw scale, then standardize to mean 0 / std 1
X_log = np.log10(cluster_df[numeric_cols])
X_log.columns = [c + "_log" for c in numeric_cols]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_log)

# ================= K-MEANS =================
silhouette_by_k = {}
for k in range(2, 8):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    silhouette_by_k[k] = silhouette_score(X_scaled, labels)
    print(f"k={k}: silhouette={silhouette_by_k[k]:.4f}")

best_k = max(silhouette_by_k, key=silhouette_by_k.get)
print("Best k by silhouette:", best_k)

km_best = KMeans(n_clusters=best_k, random_state=42, n_init=10)
kmeans_labels = km_best.fit_predict(X_scaled)

# silhouette score vs k
ks = sorted(silhouette_by_k.keys())
vals = [silhouette_by_k[k] for k in ks]
plt.figure(figsize=(7, 4.5))
plt.plot(ks, vals, marker="o")
plt.xlabel("k (number of clusters)")
plt.ylabel("Average silhouette score")
plt.title("K-means silhouette score by k")
plt.xticks(ks)
plt.tight_layout()
plt.savefig("charts/silhouette_by_k.png", dpi=150)
plt.close()

# ================= PCA (computed early so clusters can be visualized in PC space) =================
pca = PCA()
pcs = pca.fit_transform(X_scaled)
evr = pca.explained_variance_ratio_
print("Explained variance ratio:", evr)
print("Cumulative (first 2):", evr[:2].sum())

loadings = pd.DataFrame(pca.components_[:2].T, index=X_log.columns, columns=["PC1", "PC2"])
print(loadings.round(3))

# k-means clusters shown in PC1/PC2 space
plt.figure(figsize=(7, 6))
scatter = plt.scatter(pcs[:, 0], pcs[:, 1], c=kmeans_labels, s=8, alpha=0.5, cmap="tab10")
plt.xlabel("PC1"); plt.ylabel("PC2")
plt.title(f"K-means clusters (k={best_k}), shown in PC1/PC2 space")
plt.legend(*scatter.legend_elements(), title="Cluster", fontsize=8)
plt.tight_layout()
plt.savefig("charts/kmeans_clusters_pca.png", dpi=150)
plt.close()

# ================= HIERARCHICAL CLUSTERING (cosine distance) =================
# cosine distance can't be combined with ward/centroid linkage, so average
# linkage is used instead
dist = pdist(X_scaled, metric="cosine")
Z = linkage(dist, method="average")

plt.figure(figsize=(9, 5))
dendrogram(Z, truncate_mode="lastp", p=30, leaf_rotation=90, leaf_font_size=8, show_contracted=True)
plt.xlabel("Cluster (count of original points in parentheses)")
plt.ylabel("Cosine distance")
plt.title("Hierarchical clustering dendrogram (average linkage, cosine distance)")
plt.tight_layout()
plt.savefig("charts/dendrogram.png", dpi=150)
plt.close()

# read the dendrogram's own suggested k from the biggest jump in merge height
# among the last several merges
last_merges = Z[-10:, 2]
diffs = np.diff(last_merges)
jump_idx = np.argmax(diffs)
suggested_k = len(last_merges) - jump_idx
print("Dendrogram-suggested k (largest merge-height jump):", suggested_k)

# compare k-means and hierarchical clustering at the same k
hclust_labels = fcluster(Z, t=best_k, criterion="maxclust")
ari = adjusted_rand_score(kmeans_labels, hclust_labels)
print(f"Adjusted Rand Index, k-means vs hierarchical at k={best_k}:", round(ari, 4))

contingency = pd.crosstab(pd.Series(kmeans_labels, name="kmeans"),
                           pd.Series(hclust_labels, name="hclust"))
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(contingency.values, cmap="Blues")
ax.set_xticks(range(len(contingency.columns))); ax.set_xticklabels(contingency.columns)
ax.set_yticks(range(len(contingency.index))); ax.set_yticklabels(contingency.index)
ax.set_xlabel("Hierarchical cluster"); ax.set_ylabel("K-means cluster")
ax.set_title("How K-means and hierarchical clusters overlap")
for i in range(contingency.shape[0]):
    for j in range(contingency.shape[1]):
        ax.text(j, i, contingency.values[i, j], ha="center", va="center", fontsize=9)
plt.colorbar(im, label="Number of planets")
plt.tight_layout()
plt.savefig("charts/kmeans_vs_hclust.png", dpi=150)
plt.close()

# ================= PCA VISUALIZATIONS =================
plt.figure(figsize=(7, 4.5))
plt.bar(range(1, len(evr) + 1), evr)
plt.plot(range(1, len(evr) + 1), np.cumsum(evr), marker="o", color="black", label="Cumulative")
plt.xlabel("Principal component"); plt.ylabel("Proportion of variance explained")
plt.title("PCA scree plot")
plt.legend()
plt.tight_layout()
plt.savefig("charts/pca_scree.png", dpi=150)
plt.close()

plt.figure(figsize=(7, 6))
plt.scatter(pcs[:, 0], pcs[:, 1], s=6, alpha=0.3)
plt.xlabel(f"PC1 ({evr[0]*100:.1f}% variance)")
plt.ylabel(f"PC2 ({evr[1]*100:.1f}% variance)")
plt.title("Exoplanets projected onto the first two principal components")
plt.tight_layout()
plt.savefig("charts/pca_pc1_pc2.png", dpi=150)
plt.close()

fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(pcs[:, 0], pcs[:, 1], s=5, alpha=0.15, color="gray")
for feat in loadings.index:
    x, y = loadings.loc[feat, "PC1"] * 6, loadings.loc[feat, "PC2"] * 6
    ax.arrow(0, 0, x, y, color="red", width=0.02, head_width=0.15)
    ax.text(x * 1.1, y * 1.1, feat.replace("_log", ""), color="red", fontsize=9, ha="center")
ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
ax.set_title("PCA loadings: which features drive PC1 and PC2")
plt.tight_layout()
plt.savefig("charts/pca_loadings.png", dpi=150)
plt.close()

print("All Module 2 charts saved to charts/")
