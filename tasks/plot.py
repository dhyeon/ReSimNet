import seaborn as sns
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
from sklearn.manifold import TSNE
import time
import itertools
import numpy as np
from sklearn.cluster import KMeans


def plot_clustering(ingr2vec, ingr2vec_tsne, path):
	#Label Load
	labels = []
	for label in ingr2vec:
		labels.append(label)

	kmeans = KMeans(n_clusters=11, random_state=0).fit(ingr2vec_tsne)
	clusters = kmeans.labels_
	clusters = list(map(str, clusters))

	clusters_color = list(set(clusters))

	cluster2color = {
		'0' : sns.xkcd_rgb["purple"],
		'1' : sns.xkcd_rgb["forest green"],
		'2' : sns.xkcd_rgb["light pink"],
		'3' : sns.xkcd_rgb["mustard yellow"],
		'4' : sns.xkcd_rgb["orange"],
		'5' : sns.xkcd_rgb["magenta"],
		'6' : sns.xkcd_rgb["purple"],
		'7' : sns.xkcd_rgb["blue"],
		'8' : sns.xkcd_rgb["deep blue"],
		'9' : sns.xkcd_rgb["sky blue"],
		'10' : sns.xkcd_rgb["olive"],
	}

	cluster_order = [
		'0',
		'1',
		'2',
		'3',
		'4',
		'5',
		'6',
		'7',
		'8',
		'9',
		'10',


	]

	make_plot_with_labels_legends(name=path,
		  points=ingr2vec_tsne,
		  labels=labels,
		  legend_labels=clusters,
		  legend_order=cluster_order,
		  legend_label_to_color=cluster2color,
		  pretty_legend_label=pretty_category,
		  publish=False)



def plot_category(ingr2vec, ingr2vec_tsne, path, ingr2cate=None, withLegends=False):
	#Label Load
	labels = []
	for label in ingr2vec:
		labels.append(label)

	#Legend Load
	if withLegends:
		categories_all = []
		for label in labels:
			categories_all.append(ingr2cate[label])
		categories_color = list(set(categories_all))

		categories_unique = ['Dopamine receptor antagonist', 'Cyclooxygenase inhibitor', 'Histamine receptor antagonist', 'Adrenergic receptor agonist', 'Adrenergic receptor antagonist', 'Bacterial cell wall synthesis inhibitor',
								'Acetylcholine receptor antagonist', 'Glucocorticoid receptor agonist', 'Serotonin receptor antagonist', 'Sodium channel blocker', 'Others', "None FDA", "FDA"]


		categories_filtered = []
		for cate in categories_all :
			if cate in categories_unique:
				categories_filtered.append(cate)
			else:
				categories_filtered.append("Others")

		#print categories_filtered
		#print len(categories_filtered)

		category2color = {
			'Dopamine receptor antagonist' :  sns.xkcd_rgb["red"],

			'Cyclooxygenase inhibitor' : sns.xkcd_rgb["purple"],
			'Histamine receptor antagonist' : sns.xkcd_rgb["green"],
			'Adrenergic receptor agonist' : sns.xkcd_rgb["blue"],
			'Adrenergic receptor antagonist' : sns.xkcd_rgb["brown"],

			'Bacterial cell wall synthesis inhibitor' : sns.xkcd_rgb["orange"],
			'Acetylcholine receptor antagonist' : sns.xkcd_rgb["yellow"],
			'Glucocorticoid receptor agonist' : sns.xkcd_rgb["magenta"],

			'Serotonin receptor antagonist' : sns.xkcd_rgb["violet"],
			'Sodium channel blocker' : sns.xkcd_rgb["indigo"],

			'Others' : sns.xkcd_rgb["black"],

			'FDA' : sns.xkcd_rgb["red"],
			'None FDA' : sns.xkcd_rgb["grey"]
		}

		category_order = categories_unique

		make_plot_with_labels_legends(name=path,
		  points=ingr2vec_tsne,
		  labels=labels,
		  legend_labels=categories_filtered,
		  legend_order=category_order,
		  legend_label_to_color=category2color,
		  pretty_legend_label=pretty_category,
		  publish=False)

	else:
		make_plot_only_labels(name=path,
				  points=ingr2vec_tsne,
				  labels=labels,
				  publish=False)

"""
TSNE of Ingredient2Vec

"""
def load_TSNE(ingr2vec, dim=2):
	print("\nt-SNE Started... ")
	time_start = time.time()

	X = []
	for x in ingr2vec:
		X.append(ingr2vec[x][0])
	tsne = TSNE(n_components=dim)
	X_tsne = tsne.fit_transform(X)

	print("t-SNE done!")
	print("Time elapsed: {} seconds".format(time.time()-time_start))

	return X_tsne


"""
Load functions for plotting a graph
"""

flatten = lambda l: [item for sublist in l for item in sublist]

# Prettify ingredients
pretty_food = lambda s: ' '.join(s.split('_')).capitalize().lstrip()
# Prettify cuisine names
pretty_category = lambda s: ''.join(map(lambda x: x if x.islower() else " "+x, s)).lstrip()

"""
Plot Points with Labels
"""
def make_plot_only_labels(name, points, labels, publish):
	traces = []
	traces.append(go.Scattergl(
			x = points[:, 0],
			y = points[:, 1],
			mode = 'markers',
			marker = dict(
				color = sns.xkcd_rgb["black"],
				size = 8,
				opacity = 0.6,
				#line = dict(width = 1)
			),
			text = labels,
			hoverinfo = 'text',
		)
		)

	layout = go.Layout(
		xaxis=dict(
			autorange=True,
			showgrid=False,
			zeroline=False,
			showline=False,
			#autotick=True,
			ticks='',
			showticklabels=False
		),
		yaxis=dict(
			autorange=True,
			showgrid=False,
			zeroline=False,
			showline=False,
			#autotick=True,
			ticks='',
			showticklabels=False
		)
		)

	fig = go.Figure(data=traces, layout=layout)
	if publish:
		plotter = py.iplot
	else:
		plotter = offline.plot
	plotter(fig, filename=name + '.html')

"""
Plot Points with Labels and Legends
"""

def make_plot_with_labels_legends(name, points, labels, legend_labels, legend_order, legend_label_to_color, pretty_legend_label, publish):
	lst = zip(points, labels, legend_labels)
	full = sorted(lst, key=lambda x: x[2])
	traces = []
	for legend_label, group in itertools.groupby(full, lambda x: x[2]):
		group_points = []
		group_labels = []
		for tup in group:
			point, label, _ = tup
			group_points.append(point)
			group_labels.append(label)
		group_points = np.stack(group_points)
		traces.append(go.Scattergl(
			x = group_points[:, 0],
			y = group_points[:, 1],

			mode = 'markers',
			marker = dict(
				color = legend_label_to_color[legend_label],
				size = 8,
				opacity = 0.6,
				#line = dict(width = 1)
			),
			text = ['{} ({})'.format(label, pretty_legend_label(legend_label)) for label in group_labels],
			hoverinfo = 'text',
			name = legend_label
		)
		)

	# order the legend
	ordered = [[trace for trace in traces if trace.name == lab] for lab in legend_order]
	traces_ordered = flatten(ordered)
	def _set_name(trace):
		trace.name = pretty_legend_label(trace.name)
		return trace
	traces_ordered = list(map(_set_name, traces_ordered))

	"""
	annotations = []
	for index in range(50):
		new_dict = dict(
				x=points[:, 0][index],
				y=points[:, 1][index],
				xref='x',
				yref='y',
				text=labels[index],
				showarrow=True,
				arrowhead=7,
				ax=0,
				ay=-10
			)
		annotations.append(new_dict)
	"""

	layout = go.Layout(
		xaxis=dict(
			autorange=True,
			showgrid=False,
			zeroline=True,
			showline=True,
			#autotick=True,
			ticks='',
			showticklabels=False
		),
		yaxis=dict(
			autorange=True,
			showgrid=False,
			zeroline=True,
			showline=True,
			#autotick=True,
			ticks='',
			showticklabels=False
		),
		#annotations=annotations
	)
	fig = go.Figure(data=traces_ordered, layout=layout)
	if publish:
		plotter = py.iplot
	else:
		plotter = offline.plot
	plotter(fig, filename=name + '.html')
