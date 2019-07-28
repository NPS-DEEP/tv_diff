#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from tv_main_window import TVMainWindow
from export_tv_graph import export_tv_graph

# main
if __name__=="__main__":
    parser = ArgumentParser(prog='tv.py',
                   description="GUI for graphing Texture Vector similarity.")
    parser.add_argument("file1", type=str, nargs="?", default="",
                        help="The first .tv file to compare with.")
    parser.add_argument("file2", type=str, nargs="?", default="",
                        help="The second .tv file to compare with.")
    parser.add_argument("-s", "--tv_threshold_settings_file", type=str,
                        help="A texture vector threshold settings file to use.")
    parser.add_argument("-g", "--sketch_granularity", action="store_true",
                        help="Use faster sketch step granularity.")
    parser.add_argument("-z", "--zoom_count", type=int, default=0,
                        help="Number of times to zoom in.")
    non_gui_group = parser.add_mutually_exclusive_group()
    non_gui_group.add_argument("-o", "--output", action="store_true",
                        help="Output graph to default filename instead of "
                             "showing a GUI.")
    non_gui_group.add_argument("-n", "--named_output", type=str,
                        help="Output graph to named file instead of "
                             "showing a GUI.")
    non_gui_group.add_argument("-m", "--sd_metric", action="store_true",
                        help="Print the standard deviation metric instead of "
                             "showing a GUI.")
    args = parser.parse_args()

    # create the "application" and the main window
    application = QApplication(sys.argv)
    tv_main_window = TVMainWindow()

    # set granularity
    tv_main_window.action_toggle_draw_sketch.setChecked(args.sketch_granularity)
    tv_main_window.tv_data_manager.toggle_draw_sketch(args.sketch_granularity)

    # zoom in
    for i in range(args.zoom_count):
        tv_main_window.scale_manager.scale_out()

    # optionally use alternate tv settings
    f3 = args.tv_threshold_settings_file
    if f3:
        tv_main_window.settings_manager.load_from(f3)

    # optionally load tv files
    f1 = args.file1
    f2 = args.file2
    if f1 and Path(f1).is_file():
        tv_main_window.tv_data_manager.set_tv_data1(f1)
    if f2 and Path(f2).is_file():
        tv_main_window.tv_data_manager.set_tv_data2(f2)

    # start the GUI or else output the graph to file
    if args.output:
        # output default name
        graph_name = tv_main_window.suggested_tv_graph_filename()
        print("exporting plot to default file %s."%graph_name)
        export_tv_graph(graph_name, tv_main_window.tv_graph_widget.scene)

    elif args.named_output:
        # output to name
        print("exporting plot to file %s."%args.named_output)
        export_tv_graph(args.named_output, tv_main_window.tv_graph_widget.scene)

    elif args.sd_metric:
        # print metric
        sd = tv_main_window.tv_graph_widget.scene.annotation.similarity_sd
        print("Standard deviation metric: %f"%sd)

    else:
        # start the GUI
        tv_main_window.w.show()
        sys.exit(application.exec_())

