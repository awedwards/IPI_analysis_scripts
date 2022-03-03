def get_newest_cell_data(path):

    file_dict = {}
    for file in path.iterdir():
        #look for 8-character date string\n
        res = re.search("d{8}",file.name)
        if res is not None:
            file_dict[res[0]] = file.name
    try:
        recent_date = max(file_dict.keys())
        return Path(dir_path,file_dict[recent_date])

    except ValueError:
        return None
