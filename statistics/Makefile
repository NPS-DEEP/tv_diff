graphs = \
	node_hist_by_time.pdf node_hist_by_size.pdf \
	edge_hist_sim_by_sd.pdf edge_hist_sim_by_ratio.pdf
tables = node_family_table.table

.SUFFIXES: .py .pdf
.SUFFIXES: .py .table

.py.pdf:
	./$<

.py.table:
	./$<

all: $(graphs) $(tables)

clean:
	rm -f *.pdf *.png *.table

