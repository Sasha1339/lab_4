from parser import Parser
from build_query import BuildQuery


parser = Parser('PTOC11.cfg', "PTOC11.dat")

setting = 23000 #задание уставки


build = BuildQuery(parser)
build.parsering_dat_to_DB()
build.format_print_time(setting)
print(build.build_me_graphs(setting))




