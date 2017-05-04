import pymysql.cursors
def insertdata(rsid,allele,repute,magnitude,gene,chromosome,position,orientation,summary_snp,summary_genotype,pmid,omim_id):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='yao65138170',
                                 db='snpedia_wiki',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
        
            sql = "INSERT INTO snp (rsid,allele,repute,magnitude,gene,chromosome,position,orientation,summary_snp,summary_genotype,pmid,omim_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (rsid,allele,repute,magnitude,gene,chromosome,position,orientation,summary_snp,summary_genotype,pmid,omim_id))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
    except Exception as e:
        print(e)

        #    with connection.cursor() as cursor:
        # Read a single record
    #        sql = "SELECT date,shop_id, item_id FROM price WHERE shop_id=%s"
    #        cursor.execute(sql, ('123232',))
    #       result = cursor.fetchone()
    #       print(result)
    finally:
        connection.close()
        
if __name__=='__main__':
    t = "2017/01/28"
    shopid = "1232"
    itemid = "23211"
    Title = "jflsowejfow"
    Price = "232"
    insertdata(t,shopid,itemid,Title,Price)