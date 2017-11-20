# -*- coding:utf-8 -*-
# !/usr/bin/env python
import sys, getopt
from thriftpy.parser import parse
from thriftpy.Type import DataType

"""
    translate .thrift to json
"""

class DTJ:
    def __init__(self):
        self.js = []

    def parse(self, thrift_file):
        self.js = []
        result = parse(thrift_file)
        if hasattr(result, "__thrift_meta__"):
            self.metas = result.__thrift_meta__
            self.services = self.metas['services']

            return True
        else:
            return False

    def get_type_dict(self):
        self.js.append("\"structs\": {")
        self.get_struct_type_dict()
        self.js.append("},\"services\":{")
        self.get_return_type_dict()
        self.js.append("}")
        return self

    def get_return_type_dict(self):
        for service in self.services:
            self.js.extend(self.write_service(service))

    def get_struct_type_dict(self):
        structs = self.metas["structs"]
        for struct in structs:
            self.js.extend(self.write_struct(struct))
        self.trim_tail_comma(self.js)

    def output(self):
        if self.js:
            self.trim_tail_comma(self.js)
            return "{%s}" % "".join(self.js)
        return ""

    def trim_tail_comma(self, strlist):
        if strlist[-1][-1] == ",":
            tail = strlist.pop()[:-1]
            strlist.append(tail)

    def write_struct(self, struct):
        strlist = []
        if struct:
            strlist.append("\"%s\":\"" % struct.__name__.split(".")[-1])
            strlist.extend(self.write_struct_data(struct, "type"))
            strlist.append("\",")
        return strlist

    def write_service(self, service):
        strlist = []
        service_dict = vars(service)
        if service_dict:
            strlist.append("\"%s\":{" % service.__name__)
            for method_name in service_dict["thrift_services"]:
                strlist.append("\"%s\":{" % method_name)
                args_type = service_dict[method_name + '_args']
                if args_type.thrift_spec:
                    strlist.append("\"args\":\"[")
                    spec = args_type.thrift_spec
                    length = len(spec) + 1
                    for idx in range(1, length):
                        strlist.extend(self.write_type(spec[idx]))
                        if spec[idx][2] == False:
                            strlist.append("|void")
                        strlist.append(",")
                    self.trim_tail_comma(strlist)
                    strlist.append("]\",")
                result_type = service_dict[method_name + '_result']
                if result_type.thrift_spec:
                    spec = result_type.thrift_spec[0]
                    strlist.append("\"result\":\"")
                    strlist.extend(self.write_type(spec))
                    strlist.append("\"")
                    res = self.write_type(spec, "empty")
                    if res is not None:
                        strlist.append(",\"empty\":")
                        strlist.extend(self.write_type(spec, "empty"))
                strlist.append("},")
            self.trim_tail_comma(strlist)
            strlist.append("}")
            return strlist

    def write_type(self, type_spec, write_type='type'):
        param_type = type_spec[0]
        param_message = type_spec[2]
        if param_type in DataType.basicDataIndex:
            if write_type == "empty":
                return
            elif write_type == "data":
                return self.write_basic_data(param_type)
            elif write_type == "type":
                return self.write_basic_data_type(param_type)
        else:
            if write_type == "type":
                handlers = {
                    12: self.write_struct_name,
                    13: self.write_map_data,
                    14: self.write_list_data_type,
                    15: self.write_list_data_type,
                }
            else:
                handlers = {
                    12: self.write_struct_data,
                    13: self.write_map_data,
                    14: self.write_list_data,
                    15: self.write_list_data,
                }
            handler = handlers[param_type]
            return handler(param_message, write_type)

    def write_basic_data(self, param_type):
        handlers = {
            2: self.write_bool,
            3: self.write_byte,
            4: self.write_double,
            6: self.write_i16,
            8: self.write_i32,
            10: self.write_i64,
            11: self.write_str,
        }
        handler = handlers[param_type]
        return handler()

    def write_basic_data_type(self, param_type):
        handlers = {
            2: self.write_bool_type,
            3: self.write_byte_type,
            4: self.write_double_type,
            6: self.write_i16_type,
            8: self.write_i32_type,
            10: self.write_i64_type,
            11: self.write_str_type,
        }
        handler = handlers[param_type]
        return handler()

    def write_map_data(self, str_class, write_type="data"):
        return ["{" + "}"]

    def write_struct_data(self, str_class, write_type="data"):
        strlist = ["{"]
        for item in str_class.thrift_spec.items():
            field = item[1]
            res = self.write_type(field, write_type)
            if res is not None:
                fieldname = field[1]
                if write_type == "type" and not field[2]:
                    strlist.append(fieldname + "?")
                elif write_type == "empty":
                    strlist.append("\"%s\"" % fieldname)
                else:
                    strlist.append(fieldname)
                strlist.append(":")
                strlist.extend(res)
                strlist.append(",")
        # remove tail comma
        self.trim_tail_comma(strlist)
        strlist.append("}")
        return strlist

    def write_struct_name(self, str_class, write_type='type'):
        return [str_class.__name__]

    def write_list_data(self, str_class, write_type="data"):
        return ["[]"]

    def write_list_data_type(self, str_class, write_type='type'):
        strlist = ["Array<"]
        if str_class in DataType.basicDataIndex:
            strlist.extend(self.write_basic_data_type(str_class))
        else:
            param_type = str_class[0]
            param_message = str_class[1]
            if write_type == "type":
                handlers = {
                    12: self.write_struct_name,
                    13: self.write_map_data,
                    14: self.write_list_data_type,
                    15: self.write_list_data_type,
                }
            handler = handlers[param_type]
            strlist.extend(handler(param_message))
        strlist.append(">")
        return strlist

    def write_bool(self):
        return ["false"]

    def write_bool_type(self):
        return ["boolen"]

    def write_byte(self):
        return ["\"\""]

    def write_byte_type(self):
        return ["byte"]

    def write_i16(self):
        return ["-1"]

    def write_i16_type(self):
        return ["number"]

    def write_i32(self):
        return ["-1"]

    def write_i32_type(self):
        return ["number"]

    def write_i64(self):
        return ["-1"]

    def write_i64_type(self):
        return ["number"]

    def write_double(self):
        return ["-1"]

    def write_double_type(self):
        return ["number"]

    def write_str(self):
        return ["\"\""]

    def write_str_type(self):
        return ["string"]

def output_result(str_res, outputfile = None):
    if outputfile:
        with open(outputfile, 'w+') as f:
            f.write(str_res)
    else:
        print str_res

def main(argv):
    dj = DTJ()
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["input=","output="])
    except getopt.GetoptError:
        print 'python thrift_to_json.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    input_files = []
    output_files = []
    for opt, arg in opts:
        if opt == '-h':
            print 'python thrift_to_json.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--input"):
            input_files.append(arg)
        elif opt in ("-o", "--output"):
            output_files.append(arg)
    count = len(input_files)
    ocount = len(output_files)
    if count > 0:
        for i in range(0, count):
            dj.parse(input_files[i])
            if i < ocount:
                output_result(dj.get_type_dict().output(), output_files[i])
            else:
                output_result(dj.get_type_dict().output())
    else:
        for line in sys.stdin:
            filepath = line.strip()
            if filepath:
                dj.parse(filepath)
                if ocount > 0:
                    output_result(dj.get_type_dict().output(), output_files[0])
                else:
                    output_result(dj.get_type_dict().output())
if __name__ == '__main__':
    main(sys.argv[1:])
