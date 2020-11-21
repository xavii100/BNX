import pandas as pd
import numpy as np
from datetime import datetime
from app import utils
from app.log import log
from app.properties import Properties
from app.exception import WriteException, InvalidFile, NotFound
from re import search

properties = Properties()
RESPONSE = []

def apply_layout(path, file_name, type_file):
    try:
        log.info('Start apply_layout')
        RESPONSE.clear()
        demandfile = file_name.split(".xls")[0] + "_DEMAND.xlsx"
        dispersionfile =  file_name.split(".xls")[0] + "_DISPERSION.xlsx"
        log.info('obtaining path')
        path_temp = properties.PATH
        path_temp = utils.os_path_join(*path_temp)
        log.info('obtaining demand filename')
        final_path_demand = utils.get_final_path(path_temp, demandfile)
        log.info('obtaining dispersion filename')
        final_path_dispersion = utils.get_final_path(path_temp,dispersionfile)
        headers = read_excel(path, file_name)
        log.info('checking headers')
        if type_file == 'BANAMEX': 
            dfheaders = headers.iloc[0:properties.ROWS_HEADERS]
        if type_file == 'ACCIVAL':
            dfheaders = headers.iloc[0:properties.ROWS_HEADERS - 4] 
        log.info('creating df demanda')       
        df_demanda = create_data_frame(path, file_name, type_file,False)
        log.info('creating df dispersion')
        df_dispersion = create_data_frame(path, file_name, type_file,True)
            # Demanda
        cont = 0
        log.info('check creation of the files')

        log.info('path_temp: %s', path_temp)
        log.info('Info demandfile: %s', demandfile)
        log.info('Info dispersionfile: %s', dispersionfile)
        log.info('final_path_demand: %s', final_path_demand)
        log.info('final_path_dispersion: %s', final_path_dispersion)

        if len(df_demanda.index) == 1:
            log.info('Demanda not found')
            RESPONSE.append(None)
            cont = cont+1
        else:
            log.info('creating demanda file')
            writer = pd.ExcelWriter(final_path_demand)
            dfheaders.to_excel(writer, index = False)
            df_demanda.to_excel(writer, index = False, startrow=13)
            writer.save()
            writer.close()
            RESPONSE.append(demandfile)

        if len(df_dispersion.index) == 1:
            log.info('dispersion not found')
            RESPONSE.append(None)
            cont = cont+1
        else:
            log.info('creating dispersion file')
            writer = pd.ExcelWriter(final_path_dispersion)
            dfheaders.to_excel(writer, index = False)
            df_dispersion.to_excel(writer, index = False, startrow=13)
            writer.save()
            writer.close()
            RESPONSE.append(dispersionfile)
        if cont == 2:
            raise InvalidFile('Invalid file', 'File')
    except:
        raise WriteException('Invalid file', 'File')
    log.info('apply layout ends')
    return RESPONSE

''' 
    Numero de postura, Monto asignado y titulos asignados
    Si vienen llenas es dipersión

    Si no, es demanda.

    Vamos a separar las celdas primero
'''  
def create_data_frame(path, file_name, type_file,isDispersion):    
    log.info('create dataframe method starts')
    df = dataframe_postura(path, file_name, type_file,isDispersion) # Recuperación total   
    log.info('create dataframe method ends') 
    return df

def dataframe_postura(path, file_name, type_file,isDispersion):
    log.info('dataframe postura starts')
    df = read_excel(path, file_name)
    limit = df_limit(df)
    records_rejected_book_type = []
    
    col_libro= col_libro_postura(df,limit,type_file,records_rejected_book_type)
    col_consecutivo= col_consecutivo_postura(df,limit)
    col_num_nomina = col_nomina_postura(df,limit)
    col_banquero= col_nombanquero_postura(df,limit)
    col_oficina= col_oficina_postura(df,limit)
    col_division= col_division_postura(df,limit)
    col_perfilinv= col_perfilinv_postura(df,limit)
    col_operraz= col_operraz_postura(df,limit)
    col_srvinv= col_srvinv_postura(df,limit)
    col_clisati= col_clisati_postura(df,limit)
    col_cvetipoinv= col_cvetipoinv_postura(df,limit)
    col_desctipoinv= col_desctipoinv_postura(df,limit)
    col_cverelacion= col_cverelacion_postura(df,limit)
    col_dectiporelacion= col_dectiporelacion_postura(df,limit)
    col_holding= col_holding_postura(df,limit)
    col_desholding= col_desholding_postura(df,limit)
    col_promotor= col_promotor_postura(df,limit)
    col_cte= col_cte_postura(df,limit)
    col_contrato= col_contrato_postura(df,limit)
    col_monto = col_monto_sol(df,limit)
    col_mtoasignado= col_mtoasignado_postura(df,limit,isDispersion)
    col_tsa= col_tsa_postura(df,limit)
    col_fecsol= col_fecsol_postura(df,limit)
    col_hor= col_hor_postura(df,limit)
    col_descanal= col_descanal_postura(df,limit)
    col_emisora= col_emisora_postura(df,limit)
    col_serie= col_serie_postura(df,limit)
    col_postura = col_num_postura(df,limit)
    col_folio= col_folio_postura(df,limit)
    col_fecliq= col_fecliq_postura(df,limit)
    col_titulosolicitados= col_titulosolicitados_postura(df,limit)
    col_tituloasignados = col_tituloasignados_postura(df,limit)
    col_negocio= col_negocio_postura(df,limit)
    col_comentarios= col_comentarios_postura(df,limit)
    
    # Comparamos las columnas de Monto asignado, Folio y Titulos asignados
    log.info('validating columns')
    dfvalidate = pd.concat([col_mtoasignado, col_postura, col_tituloasignados],axis='columns')
    log.info('deleting condition columns')    
    # Eliminamos aquellos que no cumplen con la condición de los libros
    dfvalidate = dfvalidate.drop(dfvalidate.index[records_rejected_book_type])
    log.info('obtaining dispersion columns')
    # Obtenemos los registros que iran a Dispersion
    data_to_dispersion = dfvalidate[dfvalidate[['MTO_ASIGNADO','NUM_POSTURA','TITULOS_ASIGNADOS']].ne('').all(axis=1)]    
    log.info('obtaining demand columns')
    # Obtenemos los registros que iran a Demanda
    data_to_demanda =dfvalidate[dfvalidate[['MTO_ASIGNADO','NUM_POSTURA','TITULOS_ASIGNADOS']].eq('').all(axis=1)]           

    dfdata = dfvalidate[['MTO_ASIGNADO','NUM_POSTURA','TITULOS_ASIGNADOS']].eq('')
        
    count = 0    
    log.info('validating condition')
    for x in dfdata.index:       
        try: 
            if dfdata['MTO_ASIGNADO'][x] == True and dfdata['NUM_POSTURA'][x] == True and dfdata['TITULOS_ASIGNADOS'][x] == True:
                # Nothing to do
                m = 1
            elif dfdata['MTO_ASIGNADO'][x] == False and dfdata['NUM_POSTURA'][x] == False and dfdata['TITULOS_ASIGNADOS'][x] == False:
                # Nothing to do
                m = 1
            else:                
                count = count + 1            
        except:
            count = count + 1
            continue            
    log.info('obtaining records_rejected')
    # Obtenemos aquellos registros que no cumplen con las condiciones de Monto asignado, Folio y Titulos asignados
    records_rejected_demand_values = count
    df1 = pd.concat([col_consecutivo, col_num_nomina, col_banquero, col_oficina, col_division, 
            col_perfilinv, col_operraz, col_srvinv, col_clisati, col_cvetipoinv, col_desctipoinv, 
            col_cverelacion, col_dectiporelacion, col_holding, col_desholding, col_libro,col_promotor, 
            col_cte,col_contrato,col_mtoasignado,col_tsa,col_fecsol,col_hor,col_descanal,col_emisora,
            col_serie,col_folio,col_fecliq,col_titulosolicitados,col_negocio,col_comentarios, col_monto,
            col_tituloasignados],
            axis='columns')        

    # Por tipo de libro
    totalrecords = len(df1)
    df1 = df1.drop(df1.index[records_rejected_book_type])
    total_records_rejected_book_type = totalrecords - len(df1)    

    if(isDispersion):
        df1 = df1.loc[data_to_dispersion.index]        
        RESPONSE.append(total_records_rejected_book_type)
        RESPONSE.append(records_rejected_demand_values)
    else:                
        df1 = df1.loc[data_to_demanda.index]
    log.info('inserting trailer')
    if type_file == 'BANAMEX':
        new_row = pd.Series(['x', 'x', 'x', 'x','x', 'x', 'x', 'x', 'x','x', 'x', 'x', 'x','x', 'x', 'x', 'x', 'x','x', 'x', 'x', 'x', 'x', 'x','x', 'x', 'x', 'x', 'x','x', 'x', 'x','x'], index=df1.columns)
        df1 = df1.append(new_row, ignore_index=True)
    elif type_file == 'ACCIVAL':        
        new_row = pd.Series(['x', 'x', 'x', 'x','x', 'x', 'x', 'x', 'x','x', 'x', 'x', 'x','x', 'x', 'x', 'x', 'x','x', 'x', 'x', 'x', 'x', 'x','x', 'x', 'x', 'x', 'x','x', 'x', 'x','x'], index=df1.columns)
        df1 = df1.append(new_row, ignore_index=True)
    log.info('dataframe postura ends')
    return df1

def unique(listunique):
    list_set = set(listunique)
    unique_list = (list(list_set))
    return unique_list

def df_limit(df):
    log.info('obtaining df limit')
    data = ""
    co = 12
    while True:
        data = df.iloc[co,1]
        if(pd.isnull(data) == True):
            break
        co = co+1
    log.info('ending df limit')
    return co

def col_consecutivo_postura(df,limit):
    log.info('obtaining col_consecutivo_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            if str(df.iloc[co,0]).isspace() == True:
                list_data.append(np.nan)
                co = co+1
            else:
                list_data.append(df.iloc[co,0])
                co = co+1    
        data_final = pd.DataFrame(list_data, columns= ['NUM_CONSECUTIVO'])
        log.info('ending col_consecutivo_postura')
        return data_final
    except:
        raise InvalidFile('Error getting NUM_CONSECUTIVO', 'file')

def col_nomina_postura(df,limit):
    log.info('obtaining col_nomina_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            if str(df.iloc[co,1]).isspace() == True:
                list_data.append(np.nan)
                co = co+1
            else:
                list_data.append(df.iloc[co,1])
                co = co+1
        data_final = pd.DataFrame(list_data, columns= ['NUM_NOMINA'])
        log.info('ending col_nomina_postura')
        return data_final
    except:
        raise InvalidFile('Error getting NUM_NOMINA', 'file')


def col_nombanquero_postura(df,limit):
    log.info('obtaining col_nombanquero_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            # En caso de exederce, cortar a 50 caracteres
            data = df.iloc[co,2]
            data = data[0:50]
            list_data.append(data)
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['NUM_BANQUERO'])
        log.info('ending col_nombanquero_postura')
        return data_final
    except:
        raise InvalidFile('Error getting NUM_BANQUERO', 'file')


def col_oficina_postura(df,limit):
    log.info('obtaining col_oficina_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            # En caso de exederce, cortar a 50 caracteres
            data = df.iloc[co,3].strip()
            data = data[0:50]
            list_data.append(data)
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['DES_OFICINA'])
        log.info('ending col_oficina_postura')
        return data_final
    except:
        raise InvalidFile('Error getting DES_OFICINA', 'file')


def col_division_postura(df,limit):
    log.info('obtaining col_division_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            # En caso de exederce, cortar a 50 caracteres
            data = df.iloc[co,4].strip()
            data = data[0:50]
            list_data.append(data)
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['DES_DIVISION'])
        log.info('ending col_division_postura')
        return data_final
    except:
        raise InvalidFile('Error getting DES_DIVISION', 'file')


def col_perfilinv_postura(df,limit):
    log.info('obtaining col_perfilinv_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            # Sin espacios
            data = df.iloc[co,5]
            if type(data) is str:
                list_data.append(data.strip())
            else:
                list_data.append(data)
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['TPO_INVERSION'])
        log.info('ending col_perfilinv_postura')
        return data_final
    except:
        raise InvalidFile('Error getting TPO_INVERSION', 'file')


def col_operraz_postura(df,limit):
    log.info('obtaining col_operraz_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            # Sin espacios
            data = df.iloc[co,6]
            if type(data) is str:
                list_data.append(data.strip())
            else:
                list_data.append(data)
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['OPER'])
        log.info('ending col_operraz_postura')
        return data_final
    except:
        raise InvalidFile('Error getting OPER', 'file')


def col_srvinv_postura(df,limit):
    log.info('obtaining col_srvinv_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            if str(df.iloc[co,7]).isspace() == True:
                list_data.append(np.nan)
                co = co+1
            else:
                list_data.append(df.iloc[co,7])
                co = co+1
        data_final = pd.DataFrame(list_data, columns= ['CVE_SERVINV'])
        log.info('ending col_srvinv_postura')
        return data_final
    except:
        raise InvalidFile('Error getting CVE_SERVINV', 'file')


def col_clisati_postura(df,limit):
    log.info('obtaining col_clisati_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            # Sin espacios
            data = df.iloc[co,8]
            if type(data) is str:
                list_data.append(data.strip())
            else:
                list_data.append(data)
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['TIPO_CTE'])
        log.info('ending col_clisati_postura')
        return data_final
    except:
        raise InvalidFile('Error getting TIPO_CTE', 'file')


def col_cvetipoinv_postura(df,limit):
    log.info('obtaining col_cvetipoinv_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            if str(df.iloc[co,9]).isspace() == True:
                list_data.append(np.nan)
                co = co+1
            else:
                list_data.append(df.iloc[co,9])
                co = co+1
        data_final = pd.DataFrame(list_data, columns= ['CVE_TINVERSIONISTA'])
        log.info('ending col_cvetipoinv_postura')
        return data_final
    except:
        raise InvalidFile('Error getting CVE_TINVERSIONISTA', 'file')


def col_desctipoinv_postura(df,limit):
    log.info('obtaining col_desctipoinv_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            # Sin espacios
            data = df.iloc[co,10]
            if type(data) is str:
                list_data.append(data.strip())
            else:
                list_data.append(data)
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['DES_TINVERSIONISTA'])
        log.info('ending col_desctipoinv_postura')
        return data_final
    except:
        raise InvalidFile('Error getting DES_TINVERSIONISTA', 'file')


def col_cverelacion_postura(df,limit):
    log.info('obtaining col_cverelacion_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            if str(df.iloc[co,11]).isspace() == True:
                list_data.append(np.nan)
                co = co+1
            else:
                list_data.append(df.iloc[co,11])
                co = co+1
        data_final = pd.DataFrame(list_data, columns= ['CVE_REL'])
        log.info('ending col_cverelacion_postura')
        return data_final
    except:
        raise InvalidFile('Error getting CVE_REL', 'file')


def col_dectiporelacion_postura(df,limit):
    log.info('obtaining col_dectiporelacion_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            # Sin espacios
            data = df.iloc[co,12]
            if type(data) is str:
                list_data.append(data.strip())
            else:
                list_data.append(data)
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['DES_TPO_REL'])
        log.info('ending col_dectiporelacion_postura')
        return data_final
    except:
        raise InvalidFile('Error getting DES_TPO_REL', 'file')


def col_holding_postura(df,limit):
    log.info('obtaining col_holding_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            if str(df.iloc[co,13]).isspace() == True:
                list_data.append(np.nan)
                co = co+1
            else:
                list_data.append(df.iloc[co,13])
                co = co+1
        data_final = pd.DataFrame(list_data, columns= ['NUM_HOLDING'])
        log.info('ending col_holding_postura')
        return data_final
    except:
        raise InvalidFile('Error getting NUM_HOLDING', 'file')


def col_desholding_postura(df,limit):
    log.info('obtaining col_desholding_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            list_data.append(df.iloc[co,14])
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['DES_HOLDINGS'])
        log.info('ending col_desholding_postura')
        return data_final
    except:
        raise InvalidFile('Error getting DES_HOLDINGS', 'file')


def col_libro_postura(df,limit,type_file,records_rejected_book_type):
    log.info('obtaining col_libro_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            data = df.iloc[co,15]
            if not validaterow(data,type_file):
                records_rejected_book_type.append(co-12)
            list_data.append(data)
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['DES_LIBRO'])
        log.info('ending col_libro_postura')
        return data_final
    except:
        raise InvalidFile('Error getting DES_LIBRO', 'file')


def validaterow(data,type_file):
    log.info('validaterow method')
    return (type_file == 'ACCIVAL' and data == 'A') or (type_file == 'BANAMEX' and data == 'B')

def col_promotor_postura(df,limit):
    log.info('obtaining col_promotor_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            if str(df.iloc[co,16]).isspace() == True:
                list_data.append(np.nan)
                co = co+1
            else:
                list_data.append(df.iloc[co,16])
                co = co+1
        data_final = pd.DataFrame(list_data, columns= ['CVE_PROMOTOR'])
        log.info('ending col_promotor_postura')
        return data_final
    except:
        raise InvalidFile('Error getting CVE_PROMOTOR', 'file')


def col_cte_postura(df,limit):
    log.info('obtaining col_cte_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            if str(df.iloc[co,17]).isspace() == True:
                list_data.append(np.nan)
                co = co+1
            else:
                list_data.append(df.iloc[co,17])
                co = co+1
        data_final = pd.DataFrame(list_data, columns= ['NUM_CTE'])
        log.info('ending col_cte_postura')
        return data_final
    except:
        raise InvalidFile('Error getting NUM_CTE', 'file')

def col_contrato_postura(df,limit):
    log.info('obtaining col_contrato_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            if str(df.iloc[co,18]).isspace() == True:
                list_data.append(np.nan)
                co = co+1
            else:
                list_data.append(df.iloc[co,18])
                co = co+1
        data_final = pd.DataFrame(list_data, columns= ['NUM_CONTRATO'])
        log.info('ending col_contrato_postura')
        return data_final
    except:
        raise InvalidFile('Error getting NUM_CONTRATO', 'file')


def col_monto_sol(df,limit):
    log.info('obtaining col_monto_sol')
    co = 12
    list_data = []
    try:
        while co < limit:
            data = df.iloc[co,19]
            if pd.isna(data):
                list_data.append(np.nan)
            elif type(data) is str:
                list_data.append(data)
            else:
                number = float(data)
                number = format(number, '.2f')
                list_data.append(number)
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['MTO_SOLICITADO'])
        log.info('ending col_monto_sol')
        return data_final
    except:
        raise InvalidFile('Error getting MTO_SOLICITADO', 'file')


def col_mtoasignado_postura(df,limit,isDispersion):
    log.info('obtaining col_mtoasignado_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            # Dispersión - Lleva 2 decimales
            # Demanda - Acepta valor cero, valores negativos, decimales. En caso de decimal no completar con "0" a la derecha
            # En caso de ser dispoersión se tomma
            data = df.iloc[co,20]
            if pd.isna(data):
                list_data.append('')
            elif str(data).isspace() == True:
                list_data.append('')
            elif type(data) is str:
                list_data.append(data)
            else:
                number = float(data)                           
                number = format(number, '.2f')
                list_data.append(number)    
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['MTO_ASIGNADO'])
        log.info('ending col_mtoasignado_postura')
        return data_final
    except:
        raise InvalidFile('Error getting MTO_ASIGNADO', 'file')


def col_tsa_postura(df,limit):
    log.info('OBTAINING COL_TSA_POSTURA')
    co = 12
    list_data = []
    try:
        while co < limit:
            # Acepta valor cero, valores negativos, decimales.
            # En caso de decimal no completar con "0" a la derecha
            if str(df.iloc[co,21]).isspace() == True:
                list_data.append(np.nan)
                co = co+1
            else:
                list_data.append(df.iloc[co,21])
                co = co+1
        data_final = pd.DataFrame(list_data, columns= ['TSA'])
        log.info('ending col_tsa_postura')
        return data_final
    except:
        raise InvalidFile('Error getting TSA', 'file')

def col_fecsol_postura(df,limit):
    log.info('obtaining col_fecsol_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            stamp = df.iloc[co,22]
            stamp = str(stamp)
            try:
                stamp = stamp.replace('-', '/')
                stamp = stamp.split('.')[0]
                datetime_object = datetime.strptime(stamp, '%Y/%m/%d %H:%M:%S')
                stamp = datetime_object.strftime('%d/%m/%Y')
                list_data.append(stamp)
                co = co+1
            except:
                list_data.append(stamp)
                co = co+1
        data_final = pd.DataFrame(list_data, columns= ['FEC_SOL'])
        log.info('ending col_fecsol_postura')
        return data_final
    except:
        raise InvalidFile('Error getting FEC_SOL', 'file')


def col_hor_postura(df,limit):
    log.info('obtaining col_hor_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            hor = str(df.iloc[co,23])
            list_data.append(hor)
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['HOR'])
        log.info('ending col_hor_postura')
        return data_final
    except:
        raise InvalidFile('Error getting HOR', 'file')

def col_descanal_postura(df,limit):
    log.info('obtaining col_descanal_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            list_data.append(df.iloc[co,24])
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['DES_CANAL'])
        log.info('ending col_descanal_postura')
        return data_final
    except:
        raise InvalidFile('Error getting DES_CANAL', 'file')


def col_emisora_postura(df,limit):
    log.info('obtaining col_emisora_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            list_data.append(df.iloc[co,25])
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['NOM_EMISORA'])
        log.info('ending col_emisora_postura')
        return data_final
    except:
        raise InvalidFile('Error getting NOM_EMISORA', 'file')

def col_serie_postura(df,limit):
    log.info('obtaining col_serie_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            # Dejar los números 0 adelante
            if str(df.iloc[co,26]).isspace() == True:
                list_data.append(np.nan)
                co = co+1
            else:
                serie = str(df.iloc[co,26])
                serie = 'ç'+ serie
                list_data.append(serie)
                co = co+1
        data_final = pd.DataFrame(list_data, columns= ['SERIE'])
        log.info('ending col_serie_postura')
        return data_final
    except:
        raise InvalidFile('Error getting SERIE', 'file')

def col_num_postura(df,limit):
    log.info('obtaining col_num_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            data = df.iloc[co,27]
            if pd.isna(data):
                list_data.append('')
            elif str(data).isspace() == True:
                list_data.append('')
            else:
                list_data.append(data)
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['NUM_POSTURA'])
        log.info('ending col_num_postura')
        return data_final
    except:
        raise InvalidFile('Error getting NUM_POSTURA', 'file')


def col_folio_postura(df,limit):
    log.info('obtaining col_folio_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            if str(df.iloc[co,27]).isspace() == True:
                list_data.append('')
                co = co+1
            else:
                list_data.append(df.iloc[co,27])
                co = co+1
        data_final = pd.DataFrame(list_data, columns= ['NUM_FOLIO'])
        log.info('ending col_folio_postura')
        return data_final
    except:
        raise InvalidFile('Error getting NUM_FOLIO', 'file')


def col_fecliq_postura(df,limit):
    log.info('obtaining col_fecliq_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            stamp = df.iloc[co,28]
            stamp = str(stamp)
            try:
                stamp = stamp.replace('-', '/')
                stamp = stamp.split('.')[0]
                datetime_object = datetime.strptime(stamp, '%Y/%m/%d %H:%M:%S')
                stamp = datetime_object.strftime('%d/%m/%Y')
                list_data.append(stamp)
                co = co+1
            except:
                list_data.append(stamp)
                co = co+1
        data_final = pd.DataFrame(list_data, columns= ['FEC_LIQ'])
        log.info('ending col_fecliq_postura')
        return data_final
    except:
        raise InvalidFile('Error getting FEC_LIQ', 'file')


def col_titulosolicitados_postura(df,limit):
    log.info('obtaining col_titsolicitados')
    co = 12
    list_data = []
    try:
        while co < limit:
            if str(df.iloc[co,29]).isspace() == True:
                list_data.append(np.nan)
                co = co+1
            else:
                list_data.append(df.iloc[co,29])
                co = co+1
        data_final = pd.DataFrame(list_data, columns= ['TITULOS_SOLICITADOS'])
        log.info('ending col_titsolicitados')
        return data_final
    except:
        raise InvalidFile('Error getting TITULOS_SOLICITADOS', 'file')


def col_tituloasignados_postura(df,limit):
    log.info('obtaining col_titasigpos')
    co = 12
    list_data = []
    try:
        while co < limit:
            data = df.iloc[co,30]
            if pd.isna(data):
                list_data.append('')
            elif str(data).isspace() == True:
                list_data.append('')
            else:
                list_data.append(data)
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['TITULOS_ASIGNADOS'])
        log.info('ending col_titasigpos')
        return data_final
    except:
        raise InvalidFile('Error getting TITULOS_ASIGNADOS', 'file')


def col_negocio_postura(df,limit):
    log.info('obtaining col_negocio_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            # Sin espacios
            data = df.iloc[co,31]
            if type(data) is str:
                list_data.append(data.strip())
            else:
                list_data.append(data)
            co = co+1
        data_final = pd.DataFrame(list_data, columns= ['DES_NEGOCIO'])
        log.info('ending col_negocio_postura')
        return data_final
    except:
        raise InvalidFile('Error getting DES_NEGOCIO', 'file')


def col_comentarios_postura(df,limit):
    log.info('obtaining col_comentarios_postura')
    co = 12
    list_data = []
    try:
        while co < limit:
            data = df.iloc[co,32]
            try:
                data = str(data)
                data = data.strip()
                data = data[0:100]
                list_data.append(data)
                co = co+1
            except:
                list_data.append(df.iloc[co,32])
                co = co+1
        data_final = pd.DataFrame(list_data, columns= ['DES_COMENTARIOS'])
        log.info('ending col_comentarios_postura')
        return data_final
    except:
        raise InvalidFile('Error getting DES_COMENTARIOS', 'file')

def read_title_number_nomina(df):
    log.info('obtaining read_title_number_nomina')
    num_nomina = df.iloc[11][1]
    if type(num_nomina) == str:
        log.info('ending read_title_number_nomina')
        return num_nomina
    return None

def read_excel(path, file_name):
    log.info('reading excel')    
    excel = utils.get_final_path(path,file_name)
    df = pd.read_excel(excel, 'Archivo Prácticas de Venta')
    log.info('ending reading excel')
    return df

def read_date(df):
    log.info('reading date')
    string = df.iloc[0,12]
    string = string.replace(' de ', '/')
    datetime_object = datetime.strptime(string, '%d/%B/%Y')
    log.info('ending read date')
    return datetime_object

def append_list(list_libro, value):
    log.info('appending list')
    if isinstance(value, list):
        list_libro.append(value)
    if type(value) != str and np.isnan(value):
        list_libro.append(np.nan)
    else:
        list_libro.append(str(value))