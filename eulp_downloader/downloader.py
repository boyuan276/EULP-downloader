import os
import requests


def download_ts_agg(url_root, loc_list, type_list, local_dir):
    """
    Download NREL EULP time series aggregates

    Parameters:
        url_root (str): URL root of the file
        loc_list (list): list of location identifiers
        type_list (list): list of building types
        local_dir (str): local directory for the downloaded files

    Returns:
        local_filename_list (list): a list of downloaded file paths
        failed_filename_list (list): a list of file names failed to download
    """

    # Create local dir if not already exists
    if not os.path.isdir(local_dir):
        os.makedirs(local_dir)
        print('Created directory:', local_dir)
    else:
        print('Directory already exists:', local_dir)
    # Loop through location id and building bldg_type and download data
    local_filename_list = list()
    failed_filename_list = list()
    for loc in loc_list:
        for bldg_type in type_list:
            filename = loc.lower() + '-' + bldg_type + '.csv'
            local_filename = os.path.join(local_dir, filename)
            local_filename_list.append(local_filename)
            # Download the file if not already exists
            if not os.path.isfile(local_filename):
                req = requests.get(url_root + filename)
                # If the request is successful
                if req.status_code == 200:
                    url_content = req.content
                    csv_file = open(local_filename, 'wb')
                    csv_file.write(url_content)
                    csv_file.close()
                else:
                    failed_filename_list.append(local_filename)
                    print('File cannot be found:', filename)

    return local_filename_list, failed_filename_list


def download_bldg_ts(url_root, county_id_list, bldg_list_dict, local_dir):
    """
    Download NREL EULP building energy time series for individual buildings

    Parameters:
        url_root (str): URL root address of the downloadable files
        county_id_list (list): a list of county IDs in a state
        bldg_list_dict (dict): a dict of county IDs and the list of building
            model IDs in that county
        local_dir (str): a path of local directory to store the downloaded files

    Returns:
        local_filename_list (list): a list of downloaded file paths
        failed_filename_list (list): a list of file names failed to download
    """

    for county_id in county_id_list:
        # Create list to store filenames
        local_filename_list = list()
        failed_filename_list = list()
        # Create local dir if not already exists
        county_dir = os.path.join(local_dir, county_id)
        if not os.path.isdir(county_dir):
            os.makedirs(county_dir)
            print('Created directory:', county_dir)
        else:
            # print('Directory already exists:', county_dir)
            pass
        # Loop through counties and buildings
        bldg_id_list = bldg_list_dict[county_id]
        for bldg_id in bldg_id_list:
            county_pfx = f'county={county_id}/'
            filename = f'{bldg_id}-0.parquet'
            local_filename = os.path.join(county_dir, filename)
            local_filename_list.append(local_filename)
            # Download file if not already exists
            if not os.path.isfile(local_filename):
                web_filename = url_root + county_pfx + filename
                req = requests.get(web_filename)
                # If the request is successful
                if req.status_code == 200:
                    url_content = req.content
                    parquet_file = open(local_filename, 'wb')
                    parquet_file.write(url_content)
                    parquet_file.close()
                    print('Downloaded:', local_filename)
                else:
                    failed_filename_list.append(local_filename)
                    print('File cannot be found:', filename)
    return local_filename_list, failed_filename_list


def download_weather_ts(url_root, loc_list, bldg_type, local_dir):
    """
    Download weather time series data from NREL EULP.

    Parameters:
        url_root (str): URL root of the downloadable files
        loc_list (list): list of location identifiers
        bldg_type (list): list of building types
        local_dir (str): a path of local directory to store the files

    Returns:
        local_filename_list (list): a list of downloaded file paths
        failed_filename_list (list): a list of file names failed to download
    """

    # Create local dir if not already exists
    if not os.path.isdir(local_dir):
        os.makedirs(local_dir)
        print('Created directory:', local_dir)
    else:
        print('Directory already exists:', local_dir)
    # Loop through location id and building bldg_type and download data
    local_filename_list = list()
    failed_filename_list = list()

    for loc in loc_list:
        filename = loc + '_' + bldg_type + '.csv'
        local_filename = os.path.join(local_dir, filename)
        local_filename_list.append(local_filename)
        # Download the file if not already exists
        if not os.path.isfile(local_filename):
            req = requests.get(url_root + filename)
            # If the request is successful
            if req.status_code == 200:
                url_content = req.content
                csv_file = open(local_filename, 'wb')
                csv_file.write(url_content)
                csv_file.close()
            else:
                failed_filename_list.append(local_filename)
                print('File cannot be found:', filename)

    return local_filename_list, failed_filename_list
