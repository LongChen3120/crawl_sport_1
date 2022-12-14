

import func_detect
import crawl_lich_bxh


def parse_config(odl_object, object, data, browser):
    # hàm đọc cấu trúc config, xuất ra result tương ứng
    old_vals = object
    for key, vals in object.items():
        if isinstance(vals, str) or isinstance(vals, int):
            result = func_detect.detect_browser_result(browser, old_vals)
            return result
        elif isinstance(vals, dict):
            result = parse_config(old_vals, vals, {}, browser)
            if result:
                data[key] = result
            else:
                continue
        elif isinstance(vals, list):
            data[key] = []
            for obj in vals:
                temp = parse_config(old_vals, obj, {}, browser)
                if temp:
                    data[key].append(temp)
                else:
                    continue
    return data


# def parse_config_2(odl_object, object, data, browser):
#     # hàm đọc cấu trúc config, xuất ra result tương ứng
#     old_vals = object
#     for key, vals in object.items():
#         if isinstance(vals, str) or isinstance(vals, int):
#             result = crawl_data(browser, old_vals)
#             return result
#         elif isinstance(vals, dict):
#             result = parse_config(old_vals, vals, {}, browser)
#             if result:
#                 data[key] = result
#             else:
#                 continue
#         elif isinstance(vals, list):
#             data[key] = []
#             for obj in vals:
#                 temp = parse_config(old_vals, obj, {}, browser)
#                 if temp:
#                     data[key].append(temp)
#                 else:
#                     continue
#     return data


def parse_html(response, config):
    return crawl_lich_bxh.crawl_table(response, config)


def parse_json(response, config):
    list_data = []
    for obj in response:
        data_sample = config['data_sample'].copy()
        new_obj = crawl_lich_bxh.get_all_key_json(obj, {})
        for key, vals in config['data_sample'].items():
            if vals == "obj_json":
                obj_config = config['obj_json'][key]
                data = new_obj[obj_config['key']]
                data = func_detect.detect_type_result(data, obj_config)
            elif vals == "web":
                data = func_detect.detect_type_result(response, config[key])
            else:
                data = crawl_lich_bxh.detect_key(key, vals, data_sample, data_sample['keyword'])
                data_sample[key] = data
                continue

            if type(data) == list:
                    del data_sample[key]
                    for i in range(len(data)):
                        data_sample[key + "_" + str(i)] = data[i]
            else:
                data_sample[key] = data
        list_data.append(data_sample)
    return list_data
