import pandas as pd
import numpy as np
import os
import urllib.request
from . import config

def download_stata_file():
    """Download the Stata file directly from the URL and save it to the specified directory."""
    url = "https://www.mhasweb.org/resources/DATA/HarmonizedData/H_MHAS/Version_C2/STATA/H_MHAS_c2.dta"
    output_dir = os.path.join(config.ROOT_PATH, config.DATASET_FOLDER)

    # Crea el directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Build file path
    file_path = os.path.join(config.ROOT_PATH, os.path.basename(url))

    print("Output directory:", output_dir)
    print("File path:", file_path)
    
    # Download the file if it does not exist
    if not os.path.exists(file_path):
        try:
            urllib.request.urlretrieve(url, file_path)
            print("Stata file downloaded successfully.")
        except Exception as e:
            print("Error downloading Stata file:", e)


import pandas as pd
import os

def load_dataset(root_path, dataset_folder, dataset_name):
    """
    Load the dataset from a STATA file into a pandas DataFrame.

    Args:
        root_path (str): The root directory path where the dataset folder is located.
        dataset_folder (str): The name of the folder containing the dataset files.
        dataset_name (str): The name of the STATA file to be loaded.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the dataset file does not exist at the constructed path.
    """
    # Construct the full file path
    file_path = os.path.join(root_path, dataset_folder + "/" + dataset_name)
    print(f"Full file path: {file_path}")
    # Check if the file exists
    if os.path.exists(file_path):
        # Load the STATA file into a DataFrame
        df = pd.read_stata(file_path)
        print("Dataset loaded successfully.")
        return df
    else:
        # Raise an error if the file does not exist
        raise FileNotFoundError(f"The dataset file does not exist: {file_path}")



def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Create missing columns.
    Args:
        df (pd.DataFrame): Cleaned DataFrame.
    Returns:
        pd.DataFrame: A DataFrame with column normalization.
    """
    # Structure to facilitate the column creations and reduce computational cost
    set_columns = set()
    df_copy = df.copy()
    for column in df.columns:
        # Only check those columns with a number in the pos 1 (refers to wave´s number).
        if str(column)[1] in ('1', '2', '3', '4', '5'):
            # Identify position of the column, in which we are going to insert the new one
            pos = df_copy.columns.get_loc(column)
            # Delete the number of the wave from the column name
            aux = str(column)[0]+'x'+str(column)[2:]
            if aux not in set_columns:
                set_columns.add(aux)
                # For each column, we verify if the column is present in the five Waves.
                # For example, for the column 'rxclims', this code verifies these columns exists:
                # - r1clims
                # - r2clims
                # - r3clims
                # - r4clims
                # - r5clims
                for x in range(1,6):
                    check = str(column)[0]+str(x)+str(column)[2:]
                    # If the column to check is not present in the original datafame, we insert the column with nan values
                    if check not in df.columns:
                        # If the number > to the original column found, signifies that we are going to insert in the next pos
                        if x > int(column[1]):
                            pos+=1
                        # Insert column in an specific pos
                        df_copy.insert(loc=pos, column=check, value= np.nan)
                        # If the number < to the original column found, we update pos
                        if x < int(column[1]):
                            pos+=1
    return df_copy


def remove_columns_present_in_one_wave(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove columns that are present in only one wave.
    
    Args:
        df (pd.DataFrame): DataFrame with potentially multiple wave columns.
    
    Returns:
        pd.DataFrame: DataFrame with columns present only in one wave removed.
    """
    # Create a dictionary to count occurrences of each base column
    column_counts = {}
    
    for column in df.columns:
        # Check if the column has a wave number
        if str(column)[1] in ('1', '2', '3', '4', '5'):
            base_column = str(column)[0] + 'x' + str(column)[2:]  # Normalize to base name
            if base_column in column_counts:
                column_counts[base_column].append(column)
            else:
                column_counts[base_column] = [column]
    
    # Identify columns to drop (those present in only one wave)
    columns_to_drop = []
    for base_column, wave_columns in column_counts.items():
        if len(wave_columns) == 1:  # Only present in one wave
            columns_to_drop.extend(wave_columns)
    
    print(f"column to drop {columns_to_drop}")
    # Drop the identified columns from the DataFrame
    df_dropped = df.drop(columns=columns_to_drop, errors='ignore')
     
    return df_dropped

def split_dataset(
        df: pd.DataFrame, 
        wave_number: str
    ) -> pd.DataFrame:

    """ Split the original dataset, into n dataset, for n Waves.
    Args:
        df (pd.DataFrame): Normalized DataFrame.
        wave_number (str): Wave number.
    Returns:
        pd.DataFrame: A new DataFrame with all columns for an specific Wave.
    """

    # New DataFrame to return
    df_wave = pd.DataFrame()

    # Preserve id and inwx information
    df_wave['unhhidnp'] = df['unhhidnp']
    inw = 'inw'+str(wave_number)
    df_wave[inw] = df[inw]

    for column in df:
        # If the reference of the column name = wave_number we are checking
        if str(column)[1] == wave_number:
            # Replicate the entire column
            df_wave[column] = df[column]

    # Finally, a new column 'TARGET' is created, where our variable to predict will be stored.
    df_wave["TARGET"] = np.nan

    return df_wave


def get_target_value(
        df_wave: pd.DataFrame, 
        df_next_wave: pd.DataFrame, 
        wave_number: str
    ) -> pd.DataFrame:

    """ Get the 'TARGET' value for the wave dataset, with the next wave 'rXhosp1y' column value.
    Args:
        df_wave (pd.DataFrame): Wave DataFrame.
        df_next_wave (pd.DataFrame): Next Wave DataFrame.
        wave_number (str): Wave number.
    Returns:
        pd.DataFrame: df_wave DataFrame, with the 'TARGET' value.
    """

    # The 'TARGET' of df_wave, will be the df_next_wave 'rXhosp1y' column
    target = 'r'+str(wave_number+1)+'hosp1y'

    for index, _ in df_wave.iterrows():
        # Adding each df_next_wave 'rXhosp1y' value, into df_wave 'TARGET'
        if not pd.isna(df_next_wave[target][index]):
            df_wave['TARGET'][index] = df_next_wave[target][index]
    
    return df_wave


def filter_by_age(df_wave: pd.DataFrame, wave_number: int) -> pd.DataFrame:
    """
    Filter the DataFrame for individuals aged 50 or older in both age columns.

    Args:
        df_wave (pd.DataFrame): DataFrame for a specific wave.
        wave_number (int): The wave number (1 to 5).

    Returns:
        pd.DataFrame: Filtered DataFrame with individuals 50 years or older in both age columns.
    """
    # Construct the column names for age
    rwage_column = f'r{wave_number}agey'
    swage_column = f's{wave_number}agey'
    
    # Create a mask for individuals aged 50 or older in both columns
    mask = (df_wave[rwage_column] >= 50) & (df_wave[swage_column] >= 50)
    
    # Apply the mask and return the filtered DataFrame
    return df_wave[mask]
