# Latency Editing Library
This library will let you modify the `server_ping_latencies` field in config.json to your liking. There are two steps: 
1. Pull the latest AWS latency statistics from [cloudping.co](https://www.cloudping.co/grid/p_50/timeframe/1Y).
2. Filter the aggregate statistics into latencies that pertain to the region combinations you want to test. 

## 1. Pull the latest AWS latency statistics
These steps require using a nodejs script. For your convenience, we have already done this step, uploading AWS latency data from 4/8/2022.
1. Install node.js, following the instructions here: https://nodejs.dev/download/package-manager/.
2. Install got and cheerio
   1. `npm install got@11`
   2. `npm install cheerio`
3. Run `node all_latencies.js > all_latencies.json`. This will load the table at https://www.cloudping.co/grid/p_50/timeframe/1Y into a json file. 

## Filter aggregate latency statistics 
1. In `config.json`, edit the `server_names` parameter to include the regions you want to test with. 
   1. Note: Refer to these regions by their country in all lowercase letters. For example, `virginia`, `seoul`, `são paulo`. If the code does not recognize the region, it will produce an error. You can see exactly what region names the script is expecting by looking at the `region_to_country` dictionary in `generate_latencies.py`.  
2. Run `generate_latency.py ../config.json all_latencies.json`. This will create a copy of the `all_latencies.json` table, get rid of fields that aren't needed, and put them in the `server_latencies` field in `config.json`.