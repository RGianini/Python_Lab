# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import datetime
import os


def print_hi():
    df = pd.read_csv('intransit.tsv', sep='\t')
    df = df[df.INVOICE_NUMBER.notnull()]
    df = df.drop(['TYPE', 'CUSTOMER', 'IR', 'HOLD', 'DEMAND_SUPPLY_DATE', 'SHIP_FROM_MAKE_BUY',
                  'SHIP_FROM_PROCESSING_LEAD_TIME', 'PLANNER CHI', 'PLANNER', 'FROM_WAREHOUSE', 'LINE',
                  'PRICE LIST UNIT_PRICE', 'IR_DESCRIPTION__CUST_PO_NUMBER', 'SHIP_STATUS', 'SUPPLIER.1',
                  'UNIT_PRICE', 'PICK_LIST_DATE', 'PICK_QTY', 'DDT_DATE',
                  'DDT_ON_THE_ROAD', 'CAREL_REQUEST_DATE', 'SCHEDULED_ARRIVAL_DATE', 'ORDER_NUMBER',
                  'ORDER_BOOKING_DATE', 'REQUESTED_DATE', 'PROMISED_DATE', 'REQ_QTY'], axis=1)

    df['ITEM'] = df['ITEM'] + '*' + df['INVOICE_NUMBER'].astype(str)
    df['ITEM'] = df['ITEM'] + '*' + df['PICK_LIST_NUM'].astype(str)
    df['ITEM'] = df['ITEM'] + '*' + df['SHIPPING_METHOD'].astype(str)
    df['ITEM'] = df['ITEM'] + '*' + df['CURRENCY'].astype(str)

    df = df.drop(['INVOICE_NUMBER', 'SHIPPING_METHOD', 'CURRENCY', 'PICK_LIST_NUM'], axis=1)
    df.rename(columns={'TOTAL AMOUNT': 'TOTAL_AMOUNT'})

    df = df.groupby(['ITEM', 'SUPPLIER'])['SHIPP_QTY', 'TOTAL AMOUNT'].agg('sum').reset_index()

    df[['ITEM', 'INVOICE']] = df['ITEM'].str.split('*', 1, expand=True)
    df[['INVOICE', 'SHIPPING_METH']] = df['INVOICE'].str.split('*', 1, expand=True)
    df[['SHIPPING_METH', 'CURRENCY']] = df['SHIPPING_METH'].str.split('*', 1, expand=True)
    df[['CURRENCY', 'PICK_LIST_NUM']] = df['CURRENCY'].str.split('*', 1, expand=True)

    df.rename(columns={'SHIPPING_METH': 'PICK_LIST'}, inplace=True)
    df.rename(columns={'CURRENCY': 'SHIPPING_MET'}, inplace=True)
    df.rename(columns={'PICK_LIST_NUM': 'CURRENCY'}, inplace=True)

    # df.to_csv('out.csv', index=False)
    df_intra = df
    df_intra['ITEM'] = df_intra['ITEM'].astype(str) + '*' + df_intra['INVOICE'].astype(str)
    # df_intra = df_intra.drop['INVOICE']
    df_intra.to_csv('intraOUT.csv', index=False)

    ef = pd.read_excel('FUP.xlsx')
    ef_cmp = ef
    ef_cmp['ITEM'] = ef_cmp['ITEM'].astype(str) + '*' + ef_cmp['INVOICE_NUMBER'].astype(str)
    # ef_cmp = ef_cmp.drop['INVOICE']
    ef_cmp.to_csv('fupOUT.csv', index=False)

    tst = pd.DataFrame()
    #tst.to_csv('sera.csv', index=False)
    ind = 0
    cont_event = 0
    len_df = len(ef_cmp.index)

    for index1 in df_intra['ITEM']:
        count = 0
        for index2 in ef_cmp['ITEM']:
            if index1 == index2:
                count += 1
        if count == 0:
            cont_event += 1
            len_df += 1
            ef_cmp.loc[len_df] = [df_intra['ITEM'].iloc[ind], df_intra['SUPPLIER'].iloc[ind],
                                  df_intra['PICK_LIST'].iloc[ind], df_intra['SHIPP_QTY'].iloc[ind],
                                  df_intra['TOTAL AMOUNT'].iloc[ind], df_intra['CURRENCY'].iloc[ind],
                                  df_intra['INVOICE'].iloc[ind], df_intra['SHIPPING_MET'].iloc[ind],
                                  "", "", "", "", ""]
        ind += 1

    print("Foram Adicionadas " + str(cont_event) + " linhas.")

    ef_cmp[['ITEM', 'INVOICE']] = ef_cmp['ITEM'].str.split('*', 1, expand=True)
    ef_cmp = ef_cmp.drop(['INVOICE'], axis=1)
    ef_cmp = ef_cmp[['ITEM', 'SUPPLIER', 'PICK_LIST_NUM', 'SHIPP_QTY', 'TOTAL AMOUNT', 'CURRENCY', 'INVOICE_NUMBER',
                     'SHIPPING_METHOD', 'BOOKING', 'ETD', 'ETA', 'ETA CBR', 'REF.EMBARQUE']]

    filename = "FUP_" + str(datetime.date.today()) + ".csv"
    ef_cmp.to_csv(filename, index=False)

    os.remove('fupOUT.csv')
    os.remove('intraOUT.csv')


if __name__ == '__main__':
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
