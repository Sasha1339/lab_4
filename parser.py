from cfg import CFG


class Parser:
    def __init__(self, name_cfg, name_dat):
        self.__name_cfg = name_cfg
        self.__name_dat = name_dat

    def parsering_cfg(self):
        count = 0
        stop_read = 0
        list_of_data = []
        with open(self.__name_cfg, "r") as file_cfg:
            for line in file_cfg:
                count += 1
                if count == 2:
                    stop_read = int(line.split(",")[1][:-1])
                    self.__channel_count = stop_read
                if count <= stop_read+2 and count > 2:
                    new_line = line.split(",")
                    list_of_data.append(CFG(int(new_line[0]), new_line[1], new_line[2],new_line[3],
                                            new_line[4], float(new_line[5]),float(new_line[6]),
                                            float(new_line[7]), float(new_line[8]), float(new_line[9])))
        return list_of_data


    def get_list_of_cfg(self):
        for cfg in self.parsering_cfg():
            print(cfg)

    def get_name_dat(self):
        return self.__name_dat

    def get_channel_count(self):
        return self.__channel_count

