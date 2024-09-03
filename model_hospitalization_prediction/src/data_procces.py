import pandas as pd
from sklearn.model_selection import train_test_split

def split_train_test(df: pd.DataFrame, id_column: str, test_size: float = 0.2, random_state: int = 42):
    """
    Splits the DataFrame into training and testing sets based on unique patient IDs.

    Args:
        df (pd.DataFrame): The DataFrame to split.
        id_column (str): The name of the column containing patient IDs.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        tuple: (train_df, test_df) DataFrames for training and testing.
    """
    # Obtener IDs únicos
    unique_ids = pd.unique(df[id_column])

    # Dividir los IDs en conjuntos de entrenamiento y prueba
    train_ids, test_ids = train_test_split(unique_ids, test_size=test_size, random_state=random_state)

    # Filtrar los DataFrames originales para crear los conjuntos de entrenamiento y prueba
    train_df = df[df[id_column].isin(train_ids)]
    test_df = df[df[id_column].isin(test_ids)]

    return train_df, test_df

import os

def save_dataframes(train_df, test_df, folder='dataset', suffix=''):
    """
    Save training and test DataFrames in CSV files.

    Args:
        train_df (pd.DataFrame): DataFrame for the training set.
        test_df (pd.DataFrame): DataFrame for the test set.
        folder (str): Name of the folder where the files will be saved.
        suffix (str): Suffix to append to the file names to avoid overwriting.
    """
    # Create folder if it does not exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Generate file names with suffix 
    train_file_name = f'train_data{suffix}.csv'
    test_file_name = f'test_data{suffix}.csv'

    # Save as CSV
    train_df.to_csv(os.path.join(folder, train_file_name), index=False)
    test_df.to_csv(os.path.join(folder, test_file_name), index=False)

    print(f"Files stored in the folder '{folder}'.")


