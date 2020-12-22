import jsonify
import os
import requests
from mysql_config import mysql

oci_url = "https://itra.oraclecloud.com/itas/.anon/myservices/api/v1/products?offset=0&limit=500"
#aws_url = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/"

# all resources form OKIT
all_resources = []

def get_oci_price_list(cloud, url):
    #headers = {'Content-type': 'application/json'}
    if cloud == 'oci':
        PARAMS = {'offset': "0", 'limit': "500"}
        res = requests.get(url, PARAMS)
        #print("status code: {}".format(res.status_code))
    elif cloud == 'aws':
        res = requests.get(url)
        # print("status code: {}".format(res.status_code))
    return res.json()

def load_to_mysql(oci_price_list):
    try:
        data = []
        # search display name, metric(PAYG or monthly or requests), Model(PAY_AS_YOU_GO or MONTHLY_COMMIT)
        for oci_price in oci_price_list['items']:
            #print(oci_price)
            if 'prices' in oci_price:
                #some SKUs has no metricDisplayName
                if "metricDisplayName" in oci_price:

                    #some SKUs are free up to certain capacity, hence there are 2 PAYG, 2 Monthly Flex in a single SKU. first two prices will be 0. please go with 3rd 4th price
                    if len(oci_price['prices']) == 2:
                        # create array for bulk insert
                        row_data = (oci_price['partNumber'], oci_price['currencyCode'], oci_price['displayName'],oci_price['metricDisplayName'], oci_price['prices'][0]['value'],oci_price['prices'][1]['value'])
                    elif len(oci_price['prices']) == 4:
                        row_data = (oci_price['partNumber'], oci_price['currencyCode'], oci_price['displayName'],
                                    oci_price['metricDisplayName'], oci_price['prices'][2]['value'],
                                    oci_price['prices'][3]['value'])
                    else:
                        print("{} has more than 4 prices".format(oci_price['partNumber']))

                else:
                    row_data = (oci_price['partNumber'], oci_price['currencyCode'], oci_price['displayName'],"N/A", oci_price['prices'][0]['value'],oci_price['prices'][1]['value'])
                data.append(row_data)
            else:
                print("{} has no pricing".format(oci_price['partNumber']))
        #print(data)
        # Oracle DB => :1, :2...
        # MySQL => %s, %s...
        sql = "INSERT INTO ociprice (PARTNUMBER, CURRENCYCODE, DISPLAYNAME, METRICDISPLAYNAME, PAY_AS_YOU_GO, MONTHLY_COMMIT) values ("
        #sql += ":1, :2, :3, :4, :5, :6"
        sql += "%s, %s, %s, %s, %s, %s"
        sql += ") "
        #print(sql)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.executemany(sql, data)
        #cursor.execute(sql, data)
        conn.commit()
        selectAll = "select * from ociprice"
        cursor.execute(selectAll)
        print(cursor.fetchall())
        print("ociprice - " + str(len(data)) + " Rows Inserted")
    except Exception as e:
        print("\nError insering data into ociprice - " + str(e) + "\n")
        raise SystemExit
    finally:
        cursor.close()
        conn.close()

def cleanup_mysql():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ociprice")
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    oci_price_list = get_oci_price_list("oci", oci_url)
    #print(oci_price_list)
    #clean up data in ociprice table
    cleanup_mysql()
    #update the latest price in mysql
    load_to_mysql(oci_price_list)
