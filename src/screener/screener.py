#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator
import cutil.cutil
import finratio.comp_perf
import finratio.comp_price

from isin.isin import *
from amfi.amfi import * 

#class Screener(Isin):
class Screener(Isin, Amfi):
	def __init__(self):
		super(Screener, self).__init__()
		self.sc_name = {}
		self.sc_nsecode = []
		self.sc_cmp = {}
		self.sc_myavgiv = {}
		self.sc_iv = {}
		self.sc_mcap = {}
		self.sc_sales = {}
		self.sc_np = {}
		self.sc_pe = {}
		self.sc_pe5 = {}
		self.sc_eps = {}
		self.sc_peg = {}
		self.sc_p2bv = {}
		self.sc_p2ocf = {}
		self.sc_p2sales = {}
		self.sc_ev2ebitda = {}
		self.sc_ev = {}
		self.sc_opm = {}
		self.sc_d2e = {}
		self.sc_ic = {}
		self.sc_dp = {}
		self.sc_dp3 = {}
		self.sc_dy = {}
		self.sc_roe3 = {}
		self.sc_roce3 = {}
		self.sc_cr = {}
		self.sc_sales5 = {}
		self.sc_profit5 = {}
		self.sc_pledge = {}
		self.sc_promhold = {}
		self.sc_piotski = {}
		self.sc_altmanz = {}
		self.sc_graham = {}
		self.sc_crank = {}
		self.sc_prank = {}
		self.sc_name_aliases = {}
		# margin of safety
		self.sc_mos = {}
		self.debug_level = 0 
		self.sc_ratio_name = {'Name':'name','BSE Code': 'bse_code', 'NSE Code' : 'nse_code', 'Industry': 'industry',
							  'Current Price' : 'cmp','MyAvgIV':'myavgiv','IV Rs.':'iv',
							  'Market Capitalization':'mcap',
							  'Sales':'sales','Net profit':'np',
							  'Price to Earning':'pe','Historical PE 5Years':'pe5',
							  'EPS 12M Rs.':'eps','PEG Ratio':'peg','Price to book value':'p2bv','CMP / OCF':'p2ocf',
							  'Price to Sales':'p2sales','EVEBITDA':'ev2ebitda', 'Enterprise Value' : 'ev' ,
							  'OPM':'opm','Debt to equity':'d2e','Int Coverage':'ic','Dividend Payout Ratio':'dp',
							  'Average dividend payout 3years':'dp3','Dividend yield':'dy','Average return on equity 3Years':'roe3',
							  'ROCE3yr avg':'roce3','Current ratio':'cr','Sales growth 5Years':'sales5',
							  'Profit growth 5Years':'profit5','Pledged percentage':'pledge','Promoter Holding':'prom_hold',
							  'Piotroski score':'piotski' }
		self.sc_ratio_loc = { 'name' : 0, 'bse_code':0, 'nse_code' :0, 'industry' :0, 'cmp' : 0,'myavgiv' : 0,'iv' : 0,
							  'mcap' : 0,'sales' : 0,'np' : 0,'pe' : 0,'pe5' : 0,'eps' : 0,'peg' : 0,'p2bv' : 0,
							  'p2ocf' : 0,'p2sales' : 0,'ev2ebitda' : 0,'ev' : 0,'opm' : 0,'d2e' : 0,'icover' : 0,
							  'dp' : 0,'dp3' : 0,'dy' : 0,'roe3' : 0,'roce3' : 0,'cr' : 0,'sales5' : 0,'profit5' : 0,
							  'pledge' : 0,'prom_hold' : 0,'piotski' : 0}

	def set_debug_level(self, debug_level):
		self.debug_level = debug_level

	def load_screener_name_aliases(self, sc_aliases_filename):
		with open(sc_aliases_filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				sc_name, isin_name = row
				sc_name = sc_name.strip().capitalize()
				isin_name = isin_name.strip().capitalize()
				if self.debug_level > 1: 
					print('alias ', sc_name)
					print('real ',isin_name )
				self.sc_name_aliases[sc_name] = isin_name 
		print(self.sc_name_aliases)

	def resolve_screener_name_alias(self, company_name):
		sc_name = company_name.strip().capitalize()
		if sc_name in self.sc_name_aliases.keys():
			company_name = self.sc_name_aliases[sc_name]
		return company_name

	def load_screener_row(self, row):
		try:
			row_list = row
			if len(row_list) == 0:
				if self.debug_level > 1:
					print('ignored empty row', row_list)
				return

			sc_name = row_list[0].strip()
			if sc_name == 'Name':
				if self.debug_level > 1:
					print('picked up keys', row_list)
				rindex = 0
				for ratio in row_list:
					if ratio in self.sc_ratio_name.keys():
						if self.debug_level > 1:
							print('found ', ratio)
						self.sc_ratio_loc[self.sc_ratio_name[ratio]] = rindex
						rindex += 1
					else:
						print('check sc_ratio_name for ', ratio)
				return
			# sc_nsecode = cutil.cutil.get_number(row_list[self.sc_ratio_loc['sno']])
			# sc_name = row_list[self.sc_ratio_loc['name']]
			# screener_name = sc_name
			# sc_name = self.resolve_screener_name_alias(sc_name)
			# sc_name = cutil.cutil.normalize_comp_name(sc_name)
			# isin_code = self.get_isin_code_by_name(sc_name)
			# isin_code = self.get_amfi_isin_by_name(sc_name)
			sc_nsecode = row_list[self.sc_ratio_loc['nse_code']]
			# as sc_nsecode is no longer around: use isin_code itself
			sc_cmp = cutil.cutil.get_number(row_list[self.sc_ratio_loc['cmp']])
			# sc_myavgiv = cutil.cutil.get_number(row_list[self.sc_ratio_loc['myavgiv']])
			sc_myavgiv = 0
			# sc_iv  = cutil.cutil.get_number(row_list[self.sc_ratio_loc['iv']])
			sc_iv = 0
			sc_mcap  = cutil.cutil.get_number(row_list[self.sc_ratio_loc['mcap']])
			sc_sales  = cutil.cutil.get_number(row_list[self.sc_ratio_loc['sales']])
			sc_np = cutil.cutil.get_number(row_list[self.sc_ratio_loc['np']])
			sc_pe = cutil.cutil.get_number(row_list[self.sc_ratio_loc['pe']]) 
			sc_pe5 = cutil.cutil.get_number(row_list[self.sc_ratio_loc['pe5']]) 
			# sc_eps = cutil.cutil.get_number(row_list[self.sc_ratio_loc['eps']])
			sc_eps = 0
			sc_peg = cutil.cutil.get_number(row_list[self.sc_ratio_loc['peg']]) 
			sc_opm = cutil.cutil.get_number(row_list[self.sc_ratio_loc['opm']]) 
			sc_dp = cutil.cutil.get_number(row_list[self.sc_ratio_loc['dp']]) 
			sc_d2e = cutil.cutil.get_number(row_list[self.sc_ratio_loc['d2e']])
			# sc_ic = cutil.cutil.get_number(row_list[self.sc_ratio_loc['ic']])
			sc_ic = 0
			sc_dy = cutil.cutil.get_number(row_list[self.sc_ratio_loc['dy']]) 
			sc_p2bv = cutil.cutil.get_number(row_list[self.sc_ratio_loc['p2bv']]) 
			sc_dp3 = cutil.cutil.get_number(row_list[self.sc_ratio_loc['dp3']]) 
			sc_ev = cutil.cutil.get_number(row_list[self.sc_ratio_loc['ev']]) 
			# TBD GOLD sc_altmanz = cutil.cutil.get_number(row_list[self.sc_ratio_loc['altmanz']]) 
			sc_altmanz = 0 
			sc_cr = cutil.cutil.get_number(row_list[self.sc_ratio_loc['cr']]) 
			sc_roe3 = cutil.cutil.get_number(row_list[self.sc_ratio_loc['roe3']]) 
			sc_roce3 = cutil.cutil.get_number(row_list[self.sc_ratio_loc['roce3']]) 
			# TBD GOLD sc_graham = cutil.cutil.get_number(row_list[self.sc_ratio_loc['graham']]) 
			sc_graham = 0 
			sc_sales5 = cutil.cutil.get_number(row_list[self.sc_ratio_loc['sales5']]) 
			sc_profit5 = cutil.cutil.get_number(row_list[self.sc_ratio_loc['profit5']]) 
			sc_ev2ebitda = cutil.cutil.get_number(row_list[self.sc_ratio_loc['ev2ebitda']]) 
			sc_pledge = cutil.cutil.get_number(row_list[self.sc_ratio_loc['pledge']]) 

			self.sc_nsecode.append(sc_nsecode)

			self.sc_name[sc_nsecode] = sc_name
			self.sc_cmp[sc_nsecode] = sc_cmp
			self.sc_sales[sc_nsecode] = sc_sales
			self.sc_np[sc_nsecode] = sc_np 
			self.sc_pe[sc_nsecode] =  sc_pe
			self.sc_opm[sc_nsecode] = sc_opm 
			self.sc_eps[sc_nsecode] =  sc_eps
			self.sc_dp[sc_nsecode] =  sc_dp
			self.sc_d2e[sc_nsecode] = sc_d2e 
			self.sc_ic[sc_nsecode] = sc_ic 
			self.sc_dy[sc_nsecode] = sc_dy 
			self.sc_peg[sc_nsecode]  = sc_peg
			self.sc_p2bv[sc_nsecode]  = sc_p2bv 
			self.sc_dp3[sc_nsecode]  = sc_dp3 
			self.sc_myavgiv[sc_nsecode]  = sc_myavgiv 
			self.sc_iv[sc_nsecode]  = sc_iv 
			self.sc_ev[sc_nsecode]  = sc_ev 
			self.sc_mcap[sc_nsecode]  = sc_mcap 
			self.sc_altmanz[sc_nsecode] = sc_altmanz
			self.sc_cr[sc_nsecode] = sc_cr 
			self.sc_roe3[sc_nsecode] = sc_roe3 
			self.sc_roce3[sc_nsecode] = sc_roce3 
			self.sc_graham[sc_nsecode] = sc_graham 
			self.sc_sales5[sc_nsecode] = sc_sales5
			self.sc_profit5[sc_nsecode] = sc_profit5 
			self.sc_ev2ebitda[sc_nsecode] =  sc_ev2ebitda
			self.sc_pledge[sc_nsecode] =  sc_pledge
			# margin of safety
			# cmp(40), iv(80) - upside 100%
			# cmp(80), iv(40) - downside 50%
			if sc_myavgiv > 0:
				self.sc_mos[sc_nsecode] = int(float(sc_myavgiv-sc_cmp)*100.0/float(sc_cmp))
			else:
				self.sc_mos[sc_nsecode] = 0
			
			sc_crank = 0
			
			sc_crank += finratio.comp_perf.get_cscore_opm(sc_opm)
			sc_crank += finratio.comp_perf.get_cscore_dp(sc_dp)
			sc_crank += finratio.comp_perf.get_cscore_d2e(sc_d2e)
			sc_crank += finratio.comp_perf.get_cscore_ic(sc_ic)
			sc_crank += finratio.comp_perf.get_cscore_dp(sc_dp3)
			sc_crank += finratio.comp_perf.get_cscore_current_ratio(sc_cr)
			sc_crank += finratio.comp_perf.get_cscore_pledge(sc_pledge)
			sc_crank += finratio.comp_perf.get_cscore_altmanz(sc_altmanz)
			if sc_np > 0:
				sc_crank += 1
			if sc_eps > 0:
				sc_crank += 1
			if sc_roe3 > 6:
				sc_crank += 1 
			
			sc_prank = 0
			sc_prank += finratio.comp_price.get_pscore_pe(sc_pe)
			sc_prank += finratio.comp_price.get_pscore_peg(sc_peg)
			sc_prank += finratio.comp_price.get_pscore_pb(sc_p2bv)
			sc_prank += finratio.comp_price.get_pscore_dy(sc_dy)
			sc_prank += finratio.comp_price.get_pscore_iv(sc_cmp, sc_iv)
			sc_prank += finratio.comp_price.get_pscore_graham(sc_cmp, sc_graham)
		
			self.sc_crank[sc_nsecode] = sc_crank
			self.sc_prank[sc_nsecode] = sc_prank
			
			if self.debug_level > 1:
				print('score : ', str(sc_nsecode) , ', ', sc_name , str(sc_crank) , '\n')
			
		except IndexError:
			print('except ', row)
			traceback.print_exc()
		except KeyError:
			print('except ', row)
			traceback.print_exc()
		except:
			print('except ', row)
			traceback.print_exc()
		
	def load_isin_data_both(self, isin_bse_filename, isin_nse_filename):
		# self.load_isin_bse_data(isin_bse_filename)
		# self.load_isin_nse_data(isin_nse_filename)
		self.load_isin_db()

	def load_screener_data(self, sc_filename):
		with open(sc_filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				self.load_screener_row(row)

	def print_phase1(self, out_filename, sort_score = None):
		fh = open(out_filename, "w") 
		fh.write('sc_isin, sc_name, sc_cmp, sc_sales, sc_np, sc_pe, sc_opm, sc_eps, sc_dp3, sc_d2e, sc_ic, sc_dy, sc_peg, sc_p2bv, sc_dp3, sc_iv, sc_ev, sc_mcap, sc_altmanz, sc_cr, sc_roe3, sc_roce3, sc_graham, sc_sales5, sc_profit5, sc_ev2ebitda, sc_pledge, sc_mos, sc_crank, sc_prank\n')
		if sort_score:
			sorted_input = sorted(self.sc_crank, key=self.sc_crank.__getitem__, reverse=True)
		else:
			sorted_input = sorted(self.sc_nsecode)

		for sc_nsecode in sorted_input:
			p_str = str(sc_nsecode)
			p_str += ', ' 
			p_str += self.sc_name[sc_nsecode]
			p_str += ', ' 
			if sc_nsecode in self.sc_cmp:
				p_str += str(self.sc_cmp[sc_nsecode])
			else:
				p_str += '-'
			p_str += ', ' 
			p_str += str(self.sc_sales[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_np[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_pe[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_opm[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_eps[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_dp[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_d2e[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_ic[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_dy[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_peg[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_p2bv[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_dp3[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_iv[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_ev[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_mcap[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_altmanz[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_cr[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_roe3[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_roce3[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_graham[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_sales5[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_profit5[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_ev2ebitda[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_pledge[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_mos[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_crank[sc_nsecode])
			p_str += ', ' 
			p_str += str(self.sc_prank[sc_nsecode])
			p_str += '\n' 
			fh.write(p_str);	
		fh.close()

	def print_phase2(self, out_filename):
		self.print_phase1(out_filename, True)

	def get_sc_nsecode_by_name(self, req_name):
		for sc_nsecode in sorted(self.sc_nsecode):
			sc_name = self.sc_name[sc_nsecode]
			# try to find a matching company
			if re.match(sc_name.strip(), req_name.strip()):
				if self.debug_level > 1:
					print('sc: screener found match : ', req_name, ', sc_nsecode : ', sc_nsecode )
				return sc_nsecode
		return 0

	def get_sc_crank_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_crank:
			return self.sc_crank[sc_nsecode]
		return 0

	def get_sc_prank_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_prank:
			return self.sc_prank[sc_nsecode]
		return 0

	def get_sc_cmp_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_cmp:
			return self.sc_cmp[sc_nsecode]
		return 0
	def get_sc_iv_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_iv:
			return self.sc_iv[sc_nsecode]
		return 0

	def get_sc_dp3_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_dp3:
			return self.sc_dp3[sc_nsecode]
		return 0

	def get_sc_dp_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_dp:
			return self.sc_dp[sc_nsecode]
		return 0

	def get_sc_dy_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_dy:
			return self.sc_dy[sc_nsecode]
		return 0

	def get_sc_myavgiv_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_myavgiv:
			return self.sc_myavgiv[sc_nsecode]
		return 0

	def get_sc_d2e_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_d2e:
			return self.sc_d2e[sc_nsecode]
		return 0

	def get_sc_roe3_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_roe3:
			return self.sc_roe3[sc_nsecode]
		return 0

	def get_sc_roce3_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_roce3:
			return self.sc_roce3[sc_nsecode]
		return 0

	def get_sc_sales5_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_sales5:
			return self.sc_sales5[sc_nsecode]
		return 0

	def get_sc_profit5_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_profit5:
			return self.sc_profit5[sc_nsecode]
		return 0

	def get_sc_mos_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_mos:
			return self.sc_mos[sc_nsecode]
		return 0

	def get_sc_peg_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_peg:
			return self.sc_peg[sc_nsecode]
		return 0

	def get_sc_pledge_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_pledge:
			return self.sc_pledge[sc_nsecode]
		return 0


	def get_sc_graham_by_sno(self, sc_nsecode):
		if sc_nsecode in self.sc_graham:
			return self.sc_graham[sc_nsecode]
		return 0
