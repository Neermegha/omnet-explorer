import sys 
import configparser
import copy 
import json 
import os

class MyParser(configparser.ConfigParser):

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d 

config_count = 0
output_dir = ''
def process_config(config_index, config_dict, curr_config, orig_config):
    global config_count, output_dir
    def process_param(config, key, value):
        print(key, value)
        if len(key) > 1:
            # we have a multiparamter key ! 
            print(len(key), len(value))
            for i,k in enumerate(key):
                config[k] = value[i]
        else:
            # single parameter  
            config[key[0]] = value
        return config 
    
    p = config_dict[config_index]
    key = p['keys']
    value = p['values']
    print(key, config_index, len(value))
    config_index = config_index - 1
    for v in value:
        config = copy.deepcopy(curr_config)
        
        config = process_param(config, key, v)
        if config_index != -1:
            process_config(config_index, config_dict, config, orig_config)
        else:
            config_count = config_count+1
            orig_config[f'Config exp_{config_count}'] = dict()
            for k,v in config.items():
                orig_config[f'Config exp_{config_count}'][k] = v
            # new_config = configparser.ConfigParser()
            # new_config.read_dict(config)
            # with open(f'{output_dir}/out{config_count}.ini', 'w') as configfile:
            #     new_config.write(configfile)
 

        
def gen_configurations(ini_file, config_file, out_dir):
    global output_dir
    config = MyParser()
    config.read(ini_file)
    d = config.as_dict()

    print(d)
    with open(config_file, 'r') as f:
        search = json.load(f)
    search = search['params']
    output_dir = out_dir
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    process_config(len(search)-1, search, dict(), config)
    with open(f'{output_dir}/all_config.ini', 'w') as configfile:
        config.write(configfile)

    

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('usage: python3 gen_ini.py example.ini config.json output_dir')
        sys.exit(1)
    gen_configurations(sys.argv[1], sys.argv[2], sys.argv[3])