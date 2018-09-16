import json
import os
import re
import platform
import time
import multiprocessing
from datetime import datetime
from connection import Creating_connection

class Processing:
    def __init__(self):
        self.entry_data = None
        self.rule_data = None
        self.update_flag = 0
        my_abs_path = os.path.abspath(os.path.dirname(__file__))
        self.path_to_data_entry_file = os.path.join(my_abs_path, "entry_file.json")
        self.path_to_rule_entry_file = os.path.join(my_abs_path, "rule.json")
        self.path_to_regex_error_file = os.path.join(my_abs_path, "regex_validation_error")
        self.path_to_rule_error_file = os.path.join(my_abs_path, "rule_validation_error")
    
    def data_entry_file_handling(self):
        with open(self.path_to_data_entry_file, 'r') as f:
            self.entry_data = json.loads(f.read())
        self.update_flag = 0

    def rule_entry_file_handling(self):
        with open(self.path_to_rule_entry_file, 'r') as f:
            self.rule_data = json.loads(f.read())

    def value_as_integer(self, entry, rule):
        l = rule.split("-")
        if (int(entry) >= int(l[0])) and (int(entry) <= int(l[1])) :
            return True
        else:
            return False
    
    def value_as_string(self, entry, rule):
        return entry.upper() == rule
    
    def value_as_datetime(self, entry, rule):
        entry = datetime.strptime(entry, '%Y-%m-%d %H:%M:%S')
        rule = datetime.strptime(rule, '%Y-%m-%d %H:%M:%S')
        return entry < rule

    def insert_into_db(self, rule):
        l = [x for x in rule.keys()]
        l1 = []
        for item in l:
            l1.append(item)
            l1.append(rule[item])
        str_formation = " ".join(l1)
        time = datetime.now().strftime("%b %d %H:%M:%S")
        try:
            cur = Creating_connection.connection.cursor()
            cur.execute("INSERT INTO rule_book_mymodel(timestamp,data) VALUES('"+time+"','"+str_formation+"');")
            Creating_connection.connection.commit()
        except Exception as e:
            print(e)


    def logging(self, path_to_file, log):
        with open(path_to_file, 'a') as f:
            f.write(log)

    def data_format_checking(self, data):
        
        mat = re.match("ATL[0-9]+$",data['signal'].strip())
        
        if mat == None:
            log = str(datetime.today())+"\t"+str(data)+" ====> [Rejected] : Signal name matching issue\n"
            self.logging(self.path_to_regex_error_file,log)
            return False

        mat = re.match("Integer|String|Datetime",data['value_type'].strip())
        
        if mat == None:
            log = str(datetime.today())+"\t"+str(data)+" ====> [Rejected] : value type must be Integer | String | Datetime\n"
            self.logging(self.path_to_regex_error_file,log)
            return False

        else:
            if data['value_type'] == "Integer" and re.match("[0-9]+$",data['value'].strip()) == None:
                log = str(datetime.today())+"\t"+str(data)+" ====> [Rejected] : value must be "+\
                                "Integer for Integer value_type\n"
                self.logging(self.path_to_regex_error_file,log)
                return False
            
            if data['value_type'] == "String" and re.match("[A-Za-z]+$",data['value'].strip()) == None:
                log = str(datetime.today())+"\t"+str(data)+" ====> [Rejected] : value must  "+\
                                "consists of alphabet only for String value_type\n"
                self.logging(self.path_to_regex_error_file,log)
                return False

            if data['value_type'] == "Datetime" and re.match("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",data['value'].strip()) == None:
                log = str(datetime.today())+"\t"+str(data)+" ====> [Rejected] : value must be of format "+\
                                "YYYY-MM-DD HH:MM:SS for Datetime value_type\n"
                self.logging(self.path_to_regex_error_file,log)
                return False
        return True
        
        
    def process_data(self, lock ,v):
        for entry_rule in self.entry_data:
            if(self.data_format_checking(entry_rule)):
                if entry_rule['signal'] in self.rule_data:
                    
                    key = entry_rule['signal']
                    if entry_rule['value_type'] == self.rule_data[key][1]:
                        if entry_rule['value_type'] == "Integer":
                            if self.value_as_integer(entry_rule['value'], self.rule_data[key][0]):
                                self.insert_into_db(entry_rule)
                            else:
                                log = str(datetime.today())+"\t"+str(entry_rule)+" ====> [Rejected] : value must be in range of "\
                                                +self.rule_data[key][0]+" for "+entry_rule['signal']+" signal \n"
                                self.logging(self.path_to_rule_error_file,log)

                        if entry_rule['value_type'] == "String":
                            if self.value_as_string(entry_rule['value'], self.rule_data[key][0]):
                                self.insert_into_db(entry_rule)
                            else:
                                log = str(datetime.today())+"\t"+str(entry_rule)+" ====> [Rejected] : value for "+ \
                                        entry_rule['signal']+" signal is "+self.rule_data[key][0]+"\n"
                                self.logging(self.path_to_rule_error_file,log)

                        if entry_rule['value_type'] == "Datetime":
                            if self.value_as_datetime(entry_rule['value'], self.rule_data[key][0]):
                                self.insert_into_db(entry_rule)
                            else:
                                log = str(datetime.today())+"\t"+str(entry_rule)+" ====> [Rejected] : date "+ \
                                        "must be less then "+self.rule_data[key][0]+" for "+entry_rule['signal']+" signal\n"
                                self.logging(self.path_to_rule_error_file,log)
                    else:
                        log = str(datetime.today())+"\t"+str(entry_rule)+" ====> [Rejected] : value_type for "+entry_rule['signal']+ \
                                            " signal should be "+self.rule_data[key][1]+"\n"
                        self.logging(self.path_to_rule_error_file,log)
                else:
                    self.insert_into_db(entry_rule)
                

            lock.acquire()
            if v.value == 1:
                v.value = 0
                self.update_flag = 1
            lock.release()
            if self.update_flag == 1:
                self.rule_entry_file_handling()
                
            
def processing_entry_file(lock, v):
    Creating_connection.create_connection()
    p = Processing()
    p.data_entry_file_handling()
    p.rule_entry_file_handling()
    p.process_data(lock, v)

    lock.acquire()
    v.value = 2
    lock.release()


def rule_file_updation_check(lock, v):
    if platform.system() == 'Windows':
        ctime = os.stat("rule.json").st_ctime
        flag = 0
        while True:
            time.sleep(1)

            mtime = os.stat("rule.json").st_mtime
            if (mtime > ctime):
                ctime = mtime
                lock.acquire()
                if v.value == 0:
                    v.value = 1
                lock.release()
            lock.acquire()
            if v.value == 2:
                flag = 1
            lock.release()
            if flag == 1:
                break
	
if __name__ == "__main__":
    
    process_list = []
    v = multiprocessing.Value('i', 0)
    lock = multiprocessing.Lock()
    p1 = multiprocessing.Process(target=processing_entry_file, args=(lock, v))
    process_list.append(p1)
    
    p2 = multiprocessing.Process(target=rule_file_updation_check, args=(lock, v))
    p2.daemon = True
    process_list.append(p2)

    for process in process_list:
        process.start()
	
    for process in process_list:
        process.join()
		

