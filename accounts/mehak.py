"""Here the function has been made to extract the labourers which are close to the contractor """
import ast
import sqlite3

def show_labour(contractor_pin,no_labour_req,skill=""):
    con = sqlite3.connect('/home/mehakpreet/ppcrc/testposition/prcatice/pin_code.sqlite3') #Database connected
    cur = con.cursor()
    labour_to_be_shown = (2*no_labour_req ) # Showing twice no. of labour
    if (labour_to_be_shown <=15):  # Mininmum 15 labourers will be shown 
        labour_showing  =15
    else:
        labour_showing  = labour_to_be_shown
    
    cur.execute("SELECT near_pin FROM pincode WHERE u_pin = '{0}'".format(contractor_pin))
    result = cur.fetchone() #selecting the pincodes which are nearer to the contractors pincode
    con.close()
    if (result != None):
        list_pin = ast.literal_eval(result[0])  #extracting list of pincodes from string
        count = 0 
        total_count = 0
        final=[]
        if (skill==""):
            for pin_in_list in list_pin :    # To check the no. of labourers available in each pincode 
                connect = sqlite3.connect('/home/mehakpreet/ppcrc/testposition/prcatice/full_data_labour.sqlite3')
                cursor = connect.cursor()
                cursor.execute("SELECT *  FROM labour WHERE pin = '{0}' ORDER BY RANDOM()".format(pin_in_list))
                remaining_labour  = labour_showing - count  #remianing labour is the no. which is required to be fetched
                res = cursor.fetchmany(remaining_labour)
                count = len(res)  #no. of laboures been fetched .
                total_count  = total_count  + count # storing the count of labourers been fetched in total_count to compare it further 
                final = final + res # Storing the list of the no. of labourers been fetched in loop and then adding the other fetched labour in the next loop in 'final' 
                if (total_count >= labour_to_be_shown):#total no. labourers are equal to labour_to_be_shown then print it 
                    connect.close()
                    return(final)
                else:
                    labour_showing = remaining_labour  # so that 
            
            if (total_count  < labour_to_be_shown):
                connect.close()
                return(final)

        else:
            for pin_in_list in list_pin :    # To check the no. of labourers available in each pincode 
                connect = sqlite3.connect('/home/mehakpreet/ppcrc/testposition/prcatice/full_data_labour.sqlite3')
                cursor = connect.cursor()
                cursor.execute("SELECT * FROM labour WHERE pin = '{0}'AND skills='{1}' ORDER BY RANDOM()".format(pin_in_list,skill))
                remaining_labour  = labour_showing - count  #remianing labour is the no. which is required to be fetched
                res = cursor.fetchmany(remaining_labour)
                count = len(res)  #no. of laboures been fetched .
                total_count  = total_count  + count # storing the count of labourers been fetched in total_count to compare it further 
                final = final + res # Storing the list of the no. of labourers been fetched in loop and then adding the other fetched labour in the next loop in 'final' 
                if (total_count >= labour_to_be_shown):#total no. labourers are equal to labour_to_be_shown then print it 
                    connect.close()
                    return(final)
                else:
                    labour_showing = remaining_labour  # so that 
            
            if (total_count  < labour_to_be_shown):
                connect.close()
                return(final)
