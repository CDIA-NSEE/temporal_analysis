import pandas as pd

def test_preprocessing(df, enc, norm, ohe_list=None, te_list=None):
    # Data Transformation: One-Hot Encoding and Normalization
    df_aux = df.copy()  # Create a copy of the input DataFrame

    # Apply One-Hot Encoding (if encoder is provided)
    if ohe_list is not None:
        for col in ohe_list: # Iterate through categorical columns to be encoded

            # unknown = set(df_aux[col].unique()) - set(enc[col].categories_[0])
            # if unknown:
            #     print(f"Coluna {col} tem categorias desconhecidas: {unknown}")
            
            ohe_results = enc[col].transform(df_aux[[col]])  # Apply one-hot encoding
            df1 = pd.DataFrame(ohe_results.toarray(),  # Create a new DataFrame with the encoded features
                               columns=enc[col].get_feature_names_out(),
                               index=df_aux[col].index)
            df_aux = df_aux.merge(df1, how='left', left_index=True, right_index=True)  # Merge encoded features into the main DataFrame

        df_aux.drop(columns=ohe_list, inplace=True)  # Remove original categorical columns

    # Apply Encoding to other categorical features
    for col in te_list: #Iterate through the categorical columns
        df_aux[col] = enc[col].transform(df_aux[[col]]) #Apply the transformation

    # Apply Normalization
    norm_list = te_list + ['ANODIAG']
    df_aux[norm_list] = norm.transform(df_aux[norm_list])  # Apply normalization

    return df_aux  # Return the transformed DataFrame