import pandas as pd
from sqlalchemy import create_engine

buildingData = pd.read_csv('Building_Permits.csv')
engine = None

def trimData():
    buildingData = pd.read_csv('Building_Permits.csv')
    buildingData= buildingData[["ID", "PERMIT_TYPE", "ISSUE_DATE", "SUBTOTAL_PAID", "SUBTOTAL_UNPAID", "SUBTOTAL_WAIVED", "TOTAL_FEE", "CONTACT_1_TYPE", "CONTACT_1_NAME", "CONTACT_1_CITY", "CONTACT_1_STATE", "CONTACT_1_ZIPCODE", "WARD"]]
    buildingData = buildingData.dropna()
    print(buildingData.shape)
    buildingData.to_csv('building_permits_trimmed.csv')

def writeToDB():
    print("writing to DB")
    buildingDataTrimmed = pd.read_csv('building_permits_trimmed.csv')
    engine = create_engine('sqlite://', echo=False)
    print("created engine")
    buildingData.to_sql('buildings', con=engine)
    engine.execute("SELECT * FROM buildings WHERE SUBTOTAL_UNPAID = 0").fetchall()    
    print("put df to sql")   

def removeZeroUnpaidValues():
    print("removing zero values")
    engine.execute("DELETE FROM buildings WHERE SUBTOTAL_UNPAID = 0").fetchall()

def readFromDB():
    print("reading from db")
    buildingDataWithUnpaidAmounts = pd.read_sql_table("buildings",con=engine)
    buildingDataWithUnpaidAmounts.to_csv("building_permits_unpaid_values.csv")

def shutDownEngine():
    engine.dispose()

if __name__ == '__main__':
#    trimData()
    writeToDB()
    removeZeroUnpaidValues()
    readFromDB()
    shutDownEngine()