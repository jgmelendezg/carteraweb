import pyodbc
import pandas as pd

def obtener_cartera_vencida(fecha_corte, compania, usuario='jmelendez'):
    DATE_FMT = '%Y/%m/%d'
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=10.20.1.212;"         # Cambia por tu servidor
        "DATABASE=Contabilidad_2014;"        # Cambia por tu base
        "UID=sainventario;"             # Cambia por tu usuario
        "PWD=z;"            # Cambia por tu password
        "TrustServerCertificate=yes;"
    )
    conn = pyodbc.connect(conn_str)
    
    # Usa formato correcto para todas las fechas
    fecha_mes = fecha_corte.strftime(DATE_FMT)
    fecha_corte_str = fecha_corte.strftime(DATE_FMT)

    sql = f"""
    EXEC SP_CARTERA_VENCIMIENTO 
        @MES='{fecha_mes}',
        @RZI=' ', @RZF='zzz', @RVI=' ', @RVF='zzz', @RCTAI='13050501 ', @RCTAF='13050501 ',
        @RCI=' ', @RCF='zzzzzzzzzz ', @MOV='0', @VECEFACT='0', @VENDEZONA='2',
        @SALTOCUENTA='0', @SALTOCLIENTE='0', @SALTOZONAVENDE='0', @PROF='1', @EPORPAGINA='1', @DIAS=-99999, @CORTE='{fecha_corte_str}',
        @COMPANIA='{compania}', @CUENTA=' ', @RTerceroInicial=' ',
        @RTerceroFinal='zzzzzzzzzzzzzzzzzzzzzzzzz', @SALTOTERCERO='0', @DATOSCLIENTE='NO', @ORDENAMIENTO='IDCLIENTE',
        @TIPORESUMEN='', @FECHAFACINI='1900/01/01', @FECHAFACFIN='9999/12/31', @DIAS1=30, @DIAS2=60, @DIAS3=90,
        @TFI=' ', @TFF='zz', @ORDENGRUPO='C', @MOSTRARFACT='1', @MostrarRefFechAmbas='R', @GrEmpresarial='N',
        @GrEmpresarialIni=' ', @GrEmpresarialFin='zzzzzzzzzzzzzzzzzzzzzzzzz', @MostrarDV='N',
        @SegmentoI=' ', @SegmentoF='zzzzzzzzzzzzzzzz', @ChAgruparNumefac='N', @MostrarPorcentajes='N',
        @TIPOCLIINI=' ', @TIPOCLIFIN='zzz', @VENCI='1900/01/01', @VENCF='9999/12/31', @BU='Local', @Consolidado='N',
        @BuUsuario='N', @Usuario='{usuario}', @General='N', @IdReporte=11, @CHAgruparTipoPlazo='N', @DIAS4=180, @DIAS5=360,
        @ChExtendido='0', @IdReportDatabase=408516, @DetalladoPorBU='N'
    """
    df = pd.read_sql(sql, conn)
    conn.close()
    return df