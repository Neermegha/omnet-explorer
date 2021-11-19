# Generating all configurations 

cd ~/nni_exp

+ Pick a baseline ini file, which will be used for the experiments
+ Define a json file with the custom configurations that are needed
+ Simply execute the code to generate all the configurations 

Eg: 
``` python gen_ini.py boat/boat.ini config.json useful_dir```

In this case, the output is written to the useful_dir. Note that
if the same output directory is specified more than once, the previous 
configuration will be overwritten. 

+ As a final step, copy the contents of ```useful_dir/all_config.ini``` to OMNET++ to run the experiments. 
