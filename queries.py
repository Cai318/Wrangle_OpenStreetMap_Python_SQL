import sqlite3


def number_of_nodes():
    result = cur.execute('SELECT COUNT(*) FROM nodes')
    return result.fetchone()[0]

def number_of_nodes_tags():
    result = cur.execute('SELECT COUNT(*) FROM nodes_tags')
    return result.fetchone()[0]

def number_of_ways():
    result = cur.execute('SELECT COUNT(*) FROM ways')
    return result.fetchone()[0]

def number_of_ways_tags():
    result = cur.execute('SELECT COUNT(*) FROM ways_tags')
    return result.fetchone()[0]

def unique_users_count():
    result = cur.execute('SELECT COUNT(distinct(uid)) FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways)')
    return result.fetchone()[0]


def top_contributing_users():
    result = cur.execute('SELECT e.user, COUNT(*) as num \
                            FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e \
                            GROUP BY e.user \
                            ORDER BY num DESC \
                            LIMIT 5')

    return result.fetchall()

def top_natural():
    result = cur.execute('SELECT e.value, COUNT(*) as num \
                            FROM (SELECT value FROM nodes_tags WHERE key = "natural" \
                                  UNION ALL SELECT value FROM ways_tags WHERE key = "natural") e \
                            GROUP BY e.value \
                            ORDER BY num DESC \
                            LIMIT 5')

    return result.fetchall()

def top_tourism():
    result = cur.execute('SELECT e.value, COUNT(*) as num \
                            FROM (SELECT value FROM nodes_tags WHERE key = "tourism" \
                                  UNION ALL SELECT value FROM ways_tags WHERE key = "tourism") e \
                            GROUP BY e.value \
                            ORDER BY num DESC \
                            LIMIT 5')

    return result.fetchall()

def top_path_type():
    result = cur.execute('SELECT e.value, COUNT(*) as num \
                            FROM (SELECT value FROM nodes_tags WHERE key = "highway" \
                                  UNION ALL SELECT value FROM ways_tags WHERE key = "highway") e \
                            GROUP BY e.value \
                            ORDER BY num DESC \
                            LIMIT 5')

    return result.fetchall()

if __name__ == '__main__':

    con = sqlite3.connect("Yellowstone_SQL_DB.db")
    cur = con.cursor()
    print("\nNumber of Ways:\t\t\t", number_of_ways())
    print("Number of Nodes:\t\t", number_of_nodes())
    print("Number of Ways Tags:\t", number_of_ways_tags())
    print("Number of Nodes Tags:\t", number_of_nodes_tags())
    print("Number of Unique Users:\t", unique_users_count())
    print("\nTop Path Types:\t\t\t\t", top_path_type())
    print("Top Tourism Types:\t\t\t", top_tourism())
    print("Top Contributing Users:\t\t", top_contributing_users())
    print("Top Natural Geology Types:\t", top_natural())