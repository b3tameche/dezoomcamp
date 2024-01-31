import os
import argparse
import pandas as pd

from time import time
from sqlalchemy import create_engine

def main(params):

    # retrieve parameters
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.database
    table_name = params.table
    url = params.url

    # csv file for ingestion
    csv_path = './ny_taxi_data/taxi_zones.csv'

    # download the csv file
    os.system(f'wget {url} -O {csv_path}')

    # create engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # get iterator on dataframe
    df_iter = pd.read_csv(csv_path, iterator=True, chunksize=100000)

    # create table in the database and transfer first chunk
    df = next(df_iter)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        try:
            t_start = time()

            df = next(df_iter)
            
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append')
            t_end = time()

            print('inserted another chunk, took %.3f seconds' % (t_end - t_start))
        except StopIteration:
            print("Data was successfully ingested into the database")
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='passsword for postgres')
    parser.add_argument('--host', help='hostname for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--database', help='database name for postgres')
    parser.add_argument('--table', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)
