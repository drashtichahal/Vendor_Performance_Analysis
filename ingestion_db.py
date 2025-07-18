import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time
logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format ="%(asctime)s - %(levelname)s - %(messages)s",
    filemode ="a"
)
engine = create_engine('sqlite:///inventory.db')

def indest_db(df,table_name,engine):
    '''this function will ingest the dataframe into database table'''
    df.to_sql(table_name, con=engine, if_exists='replace', index=False, chunksize=10000)

    def load_raw_data():
    '''this function will load the csvs as dataframe and ingest into db '''
        start = time.time()
        for file in os.listdir('data'):
            if '.csv' in file:
                df = pd.read_csv('data/'+file)
                logging.info(f'Ingesting {file} in db')
                indest_db(df,file[:-4],engine)
        end = time.time()
        total_time = (end-start)/60
        logging.info("---------------ingestion complete-------------")
        logging.info(f"\nTotal Time Taken: {total_time} minutes")

if __name__ == '__main__':
    load_raw_data()