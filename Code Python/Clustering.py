from sklearn.cluster import SpectralClustering

class Clustering_:

	def __init__(self, superVectors):
		self.superVectors = superVectors
		self.ProcessClustering()
		
	def rearrange(self,labels, n):
		seen = set()
		distinct = [x for x in labels if x not in seen and not seen.add(x)]
		correct = [i for i in range(n)]
		dict_ = dict(zip(distinct, correct))
		return [x if x not in dict_ else dict_[x] for x in labels]

	def ProcessClustering(self):
		N_CLUSTERS = 2
		sc = SpectralClustering(n_clusters=N_CLUSTERS, affinity='cosine')
		labels = sc.fit_predict(self.superVectors)
		labels = self.rearrange(labels, N_CLUSTERS)
		print(labels)
		# выведем номера сегментов, где говорит девушка.
		print([i for i, x in enumerate(labels) if x == 1])
