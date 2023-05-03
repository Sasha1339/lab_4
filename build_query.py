from parser import Parser
from connectingDB import ConnectingDB
import math
import matplotlib.pyplot as plt
import pylab
class BuildQuery:
    def __init__(self, parser = Parser):
        self.__parser_cfg = parser
        self.__connect_DB = ConnectingDB

    def create_DB(self):
        new_list = self.__parser_cfg.parsering_cfg()
        drop_query = "DROP TABLE IF EXISTS DATA;"
        string_query = "CREATE TABLE DATA(ID INTEGER PRIMARY KEY, TIME INTEGER"
        count = 0
        for date in new_list:
            count += 1
            if date.get_unit_measur().rfind('A') != -1:
                for_query = ", CHANNEL_"+str(count)+"_CURRENT_PHASE_"+date.get_phase()+" REAL"
                string_query += for_query
            if date.get_unit_measur().rfind('V') != -1:
                for_query = ", CHANNEL_"+str(count)+"_VOLTAGE"+str(count)+"_PHASE_"+date.get_phase()+" REAL"
                string_query += for_query
        string_query += ");"
        self.__connect_DB.first_connect(self.__connect_DB, drop_query, string_query)
        return string_query

    def get_ALL(self):
        self.parsering_dat()
        query = "SELECT * FROM DATA"
        result = self.__connect_DB.create_query_return(self.__connect_DB, query)
        return result

    def parsing_dat(self):
        list_dat = []
        with open(self.__parser_cfg.get_name_dat(), "r") as file_dat:
            for line in file_dat:
                new_line = line.split(",")
                line_for_write = []
                for i in new_line:
                    if i == new_line[0] or i == new_line[1]:
                        line_for_write.append(int(i))
                    else:
                        try:
                            line_for_write.append(float(i))
                        except:
                            line_for_write.append(i)
                list_dat.append(line_for_write)
        return list_dat

    def build_list_to_value_a_b(self):
        list_of_dat = self.parsing_dat()
        list_of_cfg = self.__parser_cfg.parsering_cfg()
        count_channel = self.__parser_cfg.get_channel_count()
        for i in range(len(list_of_dat)):
                for j in range(count_channel):
                    list_of_dat[i][j+2]= float(list_of_cfg[j].get_a())*list_of_dat[i][j+2]+float(list_of_cfg[j].get_b())
        return list_of_dat

    def find_time_start_and_finish_phase(self, setting):
        list_of_dat = self.parsing_dat()
        list_of_cfg = self.__parser_cfg.parsering_cfg()
        time_s_f = []
        info = ""
        for i in range(len(list_of_cfg)):
            if list_of_cfg[i].get_unit_measur().rfind("A") != -1:
                time_s_f.append([])
                time_start = 1000000000.0
                flag_time_start = True
                time_finish = 0.0
                for line in list_of_dat:
                    if math.fabs(line[i+2]) > float(setting) and flag_time_start and line[1]<time_start:
                        time_start = line[1]
                        flag_time_start = False
                    if math.fabs(line[i+2]) < float(setting) and time_finish < line[1]:
                        time_finish = line[1]
                    if math.fabs(line[i+2]) > float(setting) and list_of_dat[-1] == line:
                        time_finish = line[1]
                info += "В канале "+list_of_cfg[i].get_an_equip()+"КЗ началось с"+str(time_start/1000.0)+" мс"+", закончилось"+str(time_finish/1000.0)+" мс"
                time_s_f[i].append(time_start)
                time_s_f[i].append(time_finish)
        return time_s_f

    def pol_period(self):
        list_of_dat = self.parsing_dat()
        list_of_cfg = self.__parser_cfg.parsering_cfg()
        value_more_0 = False
        time_0 = 0.0
        time_0_2 = 0.0
        for i in range(len(list_of_cfg)):
            if list_of_cfg[i].get_unit_measur().rfind("A") != -1:
                for line in list_of_dat:
                    if list_of_dat[0] == line:
                        if line[2] > 0:
                            value_more_0 = True
                    if value_more_0:
                        if line[2] <= 0:
                            time_0 = line[0]
                            break
                    else:
                        if line[2] >= 0:
                            time_0 = line[0]
                            break
                break
        for i in range(len(list_of_cfg)):
            if list_of_cfg[i].get_unit_measur().rfind("A") != -1:
                for line in list_of_dat:
                    if value_more_0:
                        if line[0] > time_0 and line[2] >= 0:
                            time_0_2 = line[0]
                            break
                    else:
                        if line[0] > time_0 and line[2] <= 0:
                            time_0_2 = line[0]
                            break
                break
        return time_0_2-time_0

    def find_max_in_period(self):
        list_of_dat = self.parsing_dat()
        list_of_cfg = self.__parser_cfg.parsering_cfg()
        pol_period = self.pol_period()
        count_I = 0
        list_max_data = []
        time_max = 0.0
        for i in range(len(list_of_cfg)):
            list_max_data.append([])
            if list_of_cfg[i].get_unit_measur().rfind("A") != -1:
                count_I += 1
                max_period = 0.0
                count = 0

                for line in list_of_dat:
                    count += 1
                    if float(count)/float(pol_period) == 1.0:
                        list_max_data[i].append([max_period, time_max])
                        max_period = 0.0
                        time_max = 0.0
                        count = 0
                    else:
                        if max_period <= math.fabs(line[i + 2]):
                            max_period = math.fabs(line[i + 2])
                            time_max = line[1]

        return list_max_data

    def find_time(self, setting):
        list_data = self.find_max_in_period()
        list_of_cfg = self.__parser_cfg.parsering_cfg()
        flag_start = False
        time_start = -1.0
        time_stop = 0.0
        time_reserv = 0.0
        count = 0
        time = []
        for i in range(len(list_of_cfg)):
            if list_of_cfg[i].get_unit_measur().rfind("A") != -1:
                count += 1
                time.append([])
                for dat in range(len(list_data)):
                    if dat == i:
                        for values in list_data[dat]:
                            time_reserv = values[1]
                            if values[0] > setting and flag_start == False:
                                time_start = values[1]
                                flag_start = True
                            if values[0] < setting and flag_start and values[1] > time_start:
                                time_stop = values[1]
                                time[count-1].append([time_start, time_stop])
                                flag_start = False
                                time_start = -1.0
                                time_stop = 0.0
                        if time_stop < time_start:
                            time_stop = time_reserv
                            time[count - 1].append([time_start, time_stop])
                            flag_start = False
                            time_start = -1.0
                            time_stop = 0.0
                        elif time_start == -1.0:
                            time[count - 1].append([0.0, 0.0])
                            flag_start = False
                            time_start = -1.0
                            time_stop = 0.0
       # print(time) #для просмотра интервалов времени соответсвующие уставке
        return time

    def format_print_time(self, setting):
        time = self.find_time(setting)
        list_of_cfg = self.__parser_cfg.parsering_cfg()
        min, max = self.more_setting_all(setting)
        result = ""
        count = 0
        for i in range(len(list_of_cfg)):
            if list_of_cfg[i].get_unit_measur().rfind("A") != -1:
                count += 1
                record = " КЗ было обнаружено: "
                for data in time[count-1]:
                    record += " c "+str(data[0])+" по "+str(data[1])+", "
                result += "По каналу номер "+str(list_of_cfg[i].get_number())+record+"\n"
        result += "Время начала КЗ для всей системы: "+str(min)+" конец КЗ: "+str(max)
        print(result)
        return result
    
    def more_setting_all(self, setting):
        time = self.find_time(setting)
        min = 1000000000000.0
        max = 0.0
        for t1 in time:
            for t2 in t1:
                if t2[0] != 0.0 or t2[1] != 0.0:
                    if min > t2[0]:
                        min = t2[0]
                    if max < t2[1]:
                        max = t2[1]
        return min, max

    def send_query_select_graphs(self, setting):
        min, max = self.more_setting_all(setting)
        query = "SELECT * FROM DATA WHERE (TIME>="+str(min)+" AND TIME<="+str(max)+")"
        result = self.__connect_DB.create_query_return(self.__connect_DB, query)
        return result

    def build_me_graphs(self, setting):
        data = self.send_query_select_graphs(setting)
        list_of_cfg = self.__parser_cfg.parsering_cfg()
        current = 0;
        voltage = 0;

        for i in range(len(list_of_cfg)):
            if list_of_cfg[i].get_unit_measur().rfind("A") != -1:
                current += 1
            if list_of_cfg[i].get_unit_measur().rfind("V") != -1:
                voltage += 1
        #if voltage == 0:
        figur, axis = plt.subplots(current)
        #else:
        #    figur, axis = plt.subplots(current, 2)
        figur.tight_layout()
        count = 0
        count_I = 0
        count_V = 0
        for i in range(len(list_of_cfg)):
            O_y = []
            O_x = []
            O_s = []
            O_s1 = []
            #if voltage == 0:
            if list_of_cfg[i].get_unit_measur().rfind("A") != -1:
                count += 1
                for line in data:
                    O_y.append(line[i+2])
                    O_x.append(line[1]/1000)
                    O_s.append(setting)
                    O_s1.append(-setting)
                axis[count-1].plot(O_x, O_y, color = "blue")
                axis[count - 1].plot(O_x, O_s, color ="red")
                axis[count - 1].plot(O_x, O_s1, color ="red")
                axis[count-1].grid()
                info = "Ток в "+str(list_of_cfg[i].get_unit_measur())+"\n ID: "+str(list_of_cfg[i].get_an_equip())
                axis[count-1].set_ylabel(info, fontsize = 10)
                if (count == current):
                    axis[count - 1].set_xlabel("Время в мс")
            # else:
            #     if list_of_cfg[i].get_unit_measur().rfind("A") != -1:
            #         count_I += 1
            #         for line in data:
            #             O_y.append(line[i+2])
            #             O_x.append(line[1]/1000)
            #             O_s.append(setting)
            #             O_s1.append(-setting)
            #         axis[0, count-1].plot(O_x, O_y, color = "blue")
            #         axis[0, count - 1].plot(O_x, O_s, color ="red")
            #         axis[0, count - 1].plot(O_x, O_s1, color ="red")
            #         axis[0, count-1].grid()
            #         info = "Ток в "+str(list_of_cfg[i].get_unit_measur())+"\n ID: "+str(list_of_cfg[i].get_an_equip())
            #         axis[0, count-1].set_ylabel(info, fontsize = 10)
            #
            #     if list_of_cfg[i].get_unit_measur().rfind("V") != -1:
            #         count_V += 1
            #         for line in data:
            #             O_y.append(line[i+2])
            #             O_x.append(line[1]/1000)
            #         axis[1, count-1].plot(O_x, O_y, color = "blue")
            #         axis[1, count - 1].plot(O_x, O_s, color ="red")
            #         axis[1, count - 1].plot(O_x, O_s1, color ="red")
            #         axis[1, count-1].grid()
            #         info = "Напряжение в "+str(list_of_cfg[i].get_unit_measur())+"\n ID: "+str(list_of_cfg[i].get_an_equip())
            #         axis[1, count-1].set_ylabel(info, fontsize = 10)

        plt.show()


    def parsering_dat_to_DB(self):
        old_query = self.create_DB()
        old_query = old_query.replace("CREATE TABLE DATA", "")
        old_query = old_query.replace(";", "")
        old_query = old_query.replace(" INTEGER PRIMARY KEY", "")
        old_query = old_query.replace(" INTEGER", "")
        old_query = old_query.replace(" REAL", "")
        j = 0
        print("Выполняется запрос на сохранение значений в Базе Данных ", end="")
        with open(self.__parser_cfg.get_name_dat(), "r") as file_dat:
            for line in file_dat:
                j += 1
                new_line = line.split(",")
                query = "INSERT INTO DATA"+old_query+" VALUES("+str(int(new_line[0]))+", "+str(int(new_line[1]))
                for i in range(self.__parser_cfg.get_channel_count()):
                    query += ", "+str(int(new_line[i+2]))
                query += ");"
                self.__connect_DB.create_query(self.__connect_DB, query)

                if j == 1:
                    print(" \rВыполняется запрос на сохранение значений в Базе Данных .", end="")
                if j == 2:
                    print(" \rВыполняется запрос на сохранение значений в Базе Данных ..", end="")
                if j == 3:
                    print(" \rВыполняется запрос на сохранение значений в Базе Данных ...", end="")
                if j == 4:
                    print(" \rВыполняется запрос на сохранение значений в Базе Данных ", end="")
                    j = 0
        print("\r                                                                           ")
        print("\r Запись данных закончена!")


