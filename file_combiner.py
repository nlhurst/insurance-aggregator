import os

import pandas as pd


class FileCombiner():
    "Format and combine insurance files into one CSV."

    def __init__(self):
        self.files = [file for file in os.listdir('input')]
        self.types_dict = {'Provider Name': str,
                    'CampaignID': str,
                    'Cost Per Ad Click': float, 
                    'Redirect Link': str,
                    'Phone Number': str,
                    'Address': str, 
                    'Zipcode': str}
        self.null_allowed_cols = ['Phone Number']
        self.required_cols = [col for col in [*self.types_dict] if col not in self.null_allowed_cols]


    def collect_files(self, files):
        """Collect CSV files from input directory and warn about invalid inputs.

        Args:
            files (list of str): Names of all files in the input directory.

        Returns:
            list of pd.DataFrame: CSV files converted to pandas dataframes.
        """
        dfs = []

        for file in files:
            try:
                df = pd.read_csv('input\\' + file, encoding='UTF-8')
            except:
                print(f'--- Error for the following file: {file} ---')
                print(f'File type is not a CSV \n \n')
                continue

            if df.empty:
                print(f'--- Error for the following file: {file} ---')
                print(f'The file is empty \n')
            else:
                empty_rows = df[df[self.required_cols].isnull().any(axis=1)]
                if df[self.required_cols].shape[0] == empty_rows.shape[0]:
                    print(f'--- Error for the following file: {file} ---')
                    print('All required rows have missing values - file will not be processed.\n')
                else:
                    print(f'--- Error for the following file: {file} ---')
                    print(f'The following rows contained empty required values - they will be dropped from the final result: \n \n {empty_rows} \n')
                    dfs.append(df)
        
        return dfs


    def format_files(self, dataframes):
        """Format each dataframe according to schema requirements.

        Args:
            dataframes (list of pd.DataFrame): CSV files that have been converted to dataframes.

        Returns:
            list of pd.DataFrame: Dataframes that have been formatted according to schema requirements.
        """
        formatted_dfs = []

        for df in dataframes:
            df = df.dropna(subset=self.required_cols)

            # format nulls for non-required columns 
            df = df.fillna('')

            df = df[[*self.types_dict]]

            for col in self.required_cols:
                df[col] = df[col].astype(str).str.replace('"', '')
                
            df = df.astype(self.types_dict)
            formatted_dfs.append(df)

        return formatted_dfs


    def create_final_csv(self, dataframes):
        """Concatenate all formatted dataframes into the final CSV.

        Args:
            dataframes (list of pd.DataFrame): Dataframes that have been formatted according to requirements.
        """
        final_df = pd.concat(dataframes)
        self.final_csv = final_df.to_csv('AggregateCsv.csv', encoding='UTF-8', index=False)


    def main(self):
        file_dfs = self.collect_files(self.files)

        if file_dfs == []:
            print('No files to process - please make sure that properly formatted CSVs are in the input directory.')
        else:
            formatted_dfs = self.format_files(file_dfs)
            self.create_final_csv(formatted_dfs)


if __name__ == '__main__':
    obj = FileCombiner()
    obj.main()
    