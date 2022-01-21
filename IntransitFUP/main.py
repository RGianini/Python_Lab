# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd


def print_hi():
    df = pd.read_csv('intransit.tsv', sep='\t')
    df_1 = df[df.INVOICE_NUMBER.notnull()]
    df_1 = df_1.drop(['TYPE', 'CUSTOMER', 'IR', 'HOLD', 'DEMAND_SUPPLY_DATE', 'SHIP_FROM_MAKE_BUY',
                      'SHIP_FROM_PROCESSING_LEAD_TIME', 'PLANNER CHI', 'PLANNER', 'FROM_WAREHOUSE', 'LINE',
                      'PRICE LIST UNIT_PRICE', 'IR_DESCRIPTION__CUST_PO_NUMBER','SHIP_STATUS', 'SUPPLIER.1',
                      'UNIT_PRICE', 'PICK_LIST_DATE', 'PICK_LIST_NUM', 'PICK_QTY', 'DDT_DATE',
                      'DDT_ON_THE_ROAD', 'CAREL_REQUEST_DATE', 'SCHEDULED_ARRIVAL_DATE', 'ORDER_NUMBER',
                      'ORDER_BOOKING_DATE', 'REQUESTED_DATE', 'PROMISED_DATE', 'REQ_QTY'], axis=1)

    df_1['ITEM'] = df_1['ITEM'] + '_' + df_1['INVOICE_NUMBER'].astype(str)
    df_1 = df_1.drop(['INVOICE_NUMBER'], axis=1)
    df_1.rename(columns={'TOTAL AMOUNT': 'TOTAL_AMOUNT'})

    df_2 = df_1.groupby(['ITEM', 'SUPPLIER'])['SHIPP_QTY', 'TOTAL AMOUNT'].agg('sum').reset_index()
    df_2[['ITEM', 'INVOICE']] = df_2['ITEM'].str.split('_', 1, expand=True)

    df_2.to_csv('out.csv', index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
