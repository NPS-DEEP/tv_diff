graphs = \
	node_hist_by_time.pdf node_hist_by_size.pdf \
	edge_hist_sim_by_sd.pdf edge_hist_sim_by_ratio.pdf
texs = \
	node_family_table.tex \
	edge_family_statistics_table.tex \
	edge_cross_family_table_sd.tex edge_cross_family_table_ratio.tex

.SUFFIXES: .py .pdf
.SUFFIXES: .py .tex

.py.pdf:
	./$<

.py.tex:
	./$<

all: $(graphs) $(texs)

clean:
	rm -f *.pdf *.png *.tex

