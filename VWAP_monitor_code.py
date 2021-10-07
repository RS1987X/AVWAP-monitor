# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 10:27:32 2021

@author: Richard
"""


import yfinance as yf
import numpy as np
import operator
import functools
import pandas as pd

#download data from yahoo finance

#=============================================================================
# =============================================================================
hist = yf.download('ATCO-A.ST VOLV-B.ST ERIC-B.ST NDA-SE.ST SAND.ST HEXA-B.ST EVO.ST EQT.ST'
                    ' ASSA-B.ST SEB-A.ST SHB-A.ST SWED-A.ST ESSITY-B.ST EPI-A.ST SEB-A.ST'
                    ' SHB-A.ST SWED-A.ST ESSITY-B.ST TELIA.ST ABB.ST AZN.ST LATO-B.ST NIBE-B.ST'
                    ' ALFA.ST SWMA.ST SKF-B.ST KINV-B.ST SCA-B.ST SINCH.ST SKA-B.ST BOL.ST ELUX-B.ST'
                    ' TEL2-B.ST BALD-B.ST INDT.ST LUND-B.ST LIFCO-B.ST GETI-B.ST HUSQ-B.ST CAST.ST'
                    ' SAGA-B.ST TREL-B.ST SECU-B.ST AAK.ST SWEC-B.ST HOLM-B.ST AXFO.ST BEIJ-B.ST ALIV-SDB.ST'
                    ' SOBI.ST EKTA-B.ST THULE.ST FABG.ST DOM.ST WALL-B.ST ADDT-B.ST KIND-SDB.ST BILL.ST TIETOS.ST'
                    ' INTRUM.ST SAAB-B.ST NENT-B.ST TIGO-SDB.ST HPOL-B.ST SBB-B.ST PEAB-B.ST AFRY.ST VITR.ST'
                    ' WIHL.ST HUFV-A.ST BRAV.ST BURE.ST SECT-B.ST JM.ST ATRLJ-B.ST CLNK-B.ST MYCR.ST KLED.ST'
                    ' LOOMIS.ST NOLA-B.ST ALIF-B.ST BHG.ST ARJO-B.ST NYF.ST MIPS.ST INSTAL.ST PNDX-B.ST'
                    ' CATE.ST STE-R.ST LUG.ST TROAX.ST LAGR-B.ST NCC-B.ST LIAB.ST MTRS.ST EPRO-B.ST'
                    ' MCOV-B.ST HMS.ST SSAB-A.ST BILI-A.ST GRNG.ST SYSR.ST MTG-B.ST BOOZT.ST KARO.ST NOBI.ST'
                    ' CAMX.ST VNV.ST RATO-B.ST CINT.ST VIT-B.ST PLAZ-B.ST BONAV-B.ST BETCO.ST RESURS.ST ONCO.ST'
                    ' DIOS.ST BIOT.ST BETS-B.ST IVSO.ST FING-B.ST SKIS-B.ST ACAD.ST BEIA-B.ST ATT.ST BIOG-B.ST INWI.ST'
                    ' CEVI.ST DUST.ST XVIVO.ST ALIG.ST CLA-B.ST AMBEA.ST CRED-A.ST SHOT.ST COIC.ST MEKO.ST BIOA-B.ST'
                    ' COOR.ST HNSA.ST NOBINA.ST OEM-B.ST CALTX.ST AQ.ST GARO.ST MSON-B.ST KNOW.ST COLL.ST SVOL-B.ST'
                    ' LEO.ST LIME.ST EOLU-B.ST G5EN.ST CTM.ST EMBRAC-B.ST NOKIA-SEK.ST PCELL.ST PDX.ST HTRO.ST ADAPT.ST'
                    ' HOFI.ST SAVE.ST TOBII.ST READ.ST CLAS-B.ST HM-B.ST ICA.ST LUNE.ST SAS.ST AZA.ST FAG.ST SF.ST'
                    ' INVE-B.ST INDU-C.ST LUMI.ST', start='2017-01-01', end='2021-10-05')
# =============================================================================

#=============================================================================


close_prices = hist["Close"].dropna(how='all').fillna(0)
volumes = hist["Volume"].dropna(how='all').fillna(0)


#download data for recent IPOs (roughly 6-12 months)
ipo_hist = yf.download('CINT.ST IDUN-B.ST SLEEP.ST RUG.ST BOAT.ST FG.ST THUNDR.ST OX2.ST ACAST.ST RVRC.ST LINC.ST'
                       ' HEM.ST CS.ST FRACTL.ST SAVE.ST FNOVA-B.ST NPAPER.ST WBGR-B.ST IMP-A-SDB.ST READ.ST VIMIAN.ST'
                       ' CARY.ST CTEK.ST KJELL.ST DSNO.ST PIERCE.ST STOR-B.ST',start='2020-10-05', end = '2021-10-07')

#STORSKOGEN
#TRUECALLER

recent_ipo_closes = ipo_hist["Close"].dropna(how='all').fillna(0)
recent_ipo_volumes = ipo_hist["Volume"].dropna(how='all').fillna(0)

#close_prices = close_prices.drop(close_prices.index[0:1180])
#volumes = volumes.drop(volumes.index[0:1180])

#calculate anchored VWAPs since year to date 
ytd_volumes = volumes[volumes.index>'2020-12-30']
ytd_closes = close_prices[close_prices.index>'2020-12-30']

ytd_avwap = []
for column in close_prices:
        ytd_avwap.append(ytd_closes[column].dot(ytd_volumes[column])/sum(ytd_volumes[column]))

#######
#Output names close to YTD AVWAP
#######
        
        
        
#calculate anchored VWAPs since IPO
ipo_avwap = []
for column in recent_ipo_closes:
    ipo_avwap.append(recent_ipo_closes[column].dot(recent_ipo_volumes[column])/sum(recent_ipo_volumes[column]))


ipo_avwap_df = pd.DataFrame([ipo_avwap], columns = recent_ipo_closes.columns)
#output recent ipos which closed within 5% of its AVWAP(IPO)
last_close = recent_ipo_closes.iloc[-1:]
close_to_avwap = np.array(abs(last_close.values/ipo_avwap_df.values-1)<0.03)
recent_ipo_names = pd.DataFrame(ipo_avwap_df.columns)
names_of_interest = recent_ipo_names.values[np.transpose(close_to_avwap)]
ipo_avwap_levels = ipo_avwap_df.values[close_to_avwap]
print(names_of_interest,ipo_avwap_levels)
