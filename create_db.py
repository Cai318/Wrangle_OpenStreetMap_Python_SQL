import pandas as pd
import sqlite3 as sq


def create_sql_db():
    con = sq.connect('Yellowstone_SQL_DB.db') # Connection object
    cur = con.cursor() # Cursor  object

    # Create empty 'nodes' table
    # Load CSV into Pandas DataFrame
    # Write DataFrame to sql db table 'nodes'
    cur.execute("CREATE TABLE if not exists nodes" +
                " (id, lat, lon, user, uid, version, changeset, timestamp)")
    nodes_df = pd.read_csv('nodes.csv')
    nodes_df.to_sql('nodes', con, if_exists='replace', index=False)

    # Repeat for nodes_tags table
    cur.execute("CREATE TABLE if not exists nodes_tags" +
                " (id, key, value, type)")
    nodes_tags_df = pd.read_csv('nodes_tags.csv')
    nodes_tags_df.to_sql('nodes_tags', con, if_exists='replace', index=False)

    # Repeat for ways table
    cur.execute("CREATE TABLE if not exists ways" +
                " (id, user, uid, version, changeset, timestamp)")
    ways_df = pd.read_csv('ways.csv')
    ways_df.to_sql('ways', con, if_exists='replace', index=False)

    # Repeat for ways_nodes table
    cur.execute("CREATE TABLE if not exists ways_nodes" +
                " (id, node_id, position)")
    ways_nodes_df = pd.read_csv('ways_nodes.csv')
    ways_nodes_df.to_sql('ways_nodes', con, if_exists='replace', index=False)

    # Repeat for ways_tags table
    cur.execute("CREATE TABLE if not exists ways_tags" +
                " (id, key, value, type)")
    ways_tags_df = pd.read_csv('ways_tags.csv')
    ways_tags_df.to_sql('ways_tags', con, if_exists='replace', index=False)


create_sql_db()
print('\nSQL database and tables have created. Lets query!')




