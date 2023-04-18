import os
import numpy as np
import pandas as pd
import downloader as dl
import requests

#### Parameter setup

# Choose the state of study, only supports NY or CA
state = 'ny'
# state = 'ca'

# Download tmy3 data or not
download_tmy = False

# Create directories to store the data
data_dir = '/mnt/data1/EULP/2022/'
resstock_amy2018_dir = os.path.join(data_dir, 'resstock_amy2018_release_1')
resstock_amy2012_dir = os.path.join(data_dir, 'resstock_amy2012_release_1')
resstock_tmy3_dir = os.path.join(data_dir, 'resstock_tmy3_release_1')

# Setup urls
url_root = 'https://oedi-data-lake.s3.amazonaws.com/nrel-pds-building-stock/end-use-load-profiles-for-us-building-stock/2022/'
resstock_amy2018_pfx = url_root + 'resstock_amy2018_release_1/'
resstock_amy2012_pfx = url_root + 'resstock_amy2012_release_1/'
resstock_tmy3_pfx = url_root + 'resstock_tmy3_release_1/'

# List of upgrades
upgrade_list = ['upgrade%02d' %x for x in range(1, 11)]
upgrade_list.insert(0, 'baseline')

upgrade_list_num = ['upgrade=%d' %x for x in range(0, 11)]

#### Download metadata and annual result
format = 'parquet'
# format = 'csv'

# Create local dir if not already exists
local_dir = os.path.join(resstock_amy2018_dir, 
                        'metadata_and_annual_results',
                        'by_state',
                        f'state={state.upper()}',
                        format)

if not os.path.isdir(local_dir):
    os.makedirs(local_dir)
    print('Created directory:', local_dir)
else:
    print('Directory already exists:', local_dir)

# URL for metadata and annual results (state specific)
url_metadata = resstock_amy2018_pfx + 'metadata_and_annual_results/' \
    + f'by_state/state={state.upper()}/{format}/'

# Loop through location id and building bldg_type and download data
local_filename_list = list()
failed_filename_list = list()

for upgrade in upgrade_list:
    filename = f'{state.upper()}_{upgrade}_metadata_and_annual_results.{format}'
    local_filename = os.path.join(local_dir, filename)
    local_filename_list.append(local_filename)

    # Download the file if not already exists
    if not os.path.isfile(local_filename):
        req = requests.get(url_metadata + filename)

        # If the request is successful
        if req.status_code == 200:
            url_content = req.content
            csv_file = open(local_filename, 'wb')
            csv_file.write(url_content)
            csv_file.close()
        else:
            failed_filename_list.append(local_filename)
            print('File cannot be found:', filename)

metadata_and_annual_result_df = pd.read_parquet(local_filename_list[0], 
                                                engine='pyarrow')
metadata_and_annual_result_df

#### Download individual building time series
bldg_id_list = metadata_and_annual_result_df.index.to_list()

failed_filename_list = list()

# Loop through upgrade types
for i, upgrade_num in enumerate(upgrade_list_num):

    print(f'Start downloading {upgrade_num} ...')

    upgrade_num = upgrade_list_num[i]

    # Create local dir if not already exists
    local_dir = os.path.join(resstock_amy2018_dir, 
                            'timeseries_individual_buildings',
                            'by_state',
                            upgrade_num,
                            f'state={state.upper()}')

    if not os.path.isdir(local_dir):
        os.makedirs(local_dir)
        print('Created directory:', local_dir)
    else:
        print('Directory already exists:', local_dir)

    # URL for metadata and annual results (state specific)
    url_pfx = resstock_amy2018_pfx + 'timeseries_individual_buildings/' \
        + f'by_state/{upgrade_num}/state={state.upper()}/'

    local_filename_list = list()

    # Loop through building ids
    for bldg_id in bldg_id_list:
        filename = f'{bldg_id}-{i}.parquet'
        local_filename = os.path.join(local_dir, filename)
        local_filename_list.append(local_filename)

        # Download the file if not already exists
        if not os.path.isfile(local_filename):
            req = requests.get(url_pfx + filename)

            # If the request is successful
            if req.status_code == 200:
                url_content = req.content
                csv_file = open(local_filename, 'wb')
                csv_file.write(url_content)
                csv_file.close()
            else:
                failed_filename_list.append(local_filename)
                print('File cannot be found:', filename)

    print(f'Finished downloading {upgrade_num}!')
