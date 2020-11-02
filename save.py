import pickle


def load_dict_from_pkl(file_path):
    try:
        with open(file_path, "rb") as load_file:
            output = dict(pickle.load(load_file))
            load_file.close()
        return output
    except FileNotFoundError:
        raise FileNotFoundError


def save_dict_to_pkl(input_dict, file_path):
    try:
        with open(file_path, "wb") as save_file:
            pickle.dump(input_dict, save_file)
            save_file.close()
    except FileNotFoundError:
        raise FileNotFoundError


def merge_to_pkl_dictionary(input_dict, file_path):
    try:
        new_dict = load_dict_from_pkl(file_path)
        new_dict.update(input_dict)
        save_dict_to_pkl(new_dict, file_path)
    except FileNotFoundError:
        save_dict_to_pkl(input_dict, file_path)