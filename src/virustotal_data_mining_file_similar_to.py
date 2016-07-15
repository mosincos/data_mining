#!/usr/local/bin/python

import sys, time

from config_file import *
sys.path.append(bin_dir)
from functions_lib  import *


analyzer = import_from("virustotal_data_mining_analyzer")

md5_lst = analyzer.get_md5_from_high_scored_data(high_scored_hashes)
if md5_lst == False:
   print high_scored_hashes+" doesn't exist. Please schedule running this script after virustotal_data_mining_file.py"
   sys.exit()

for hash_name in md5_lst:
    search_tbl = {"similar-to": hash_name}
    page_counter = 0
    next_page = None
    while page_counter <= 4:
         page_counter+=1
         next_page, hashes = analyzer.get_matching_files(search_tbl, page=next_page)
         if len(hashes)==0:
            page_counter = 5
            continue
         if next_page == None and page_counter>1:
            continue
         for md5 in hashes:
            report = analyzer.get_report(md5)
            if len(report) == 0:
                 continue
            positives = report.get("positives")
            if positives > 6:
                 scan_report = report.get("scans")
                 av_score = analyzer.get_av_engine_score(scan_report)
                 if (av_score >=6  and av_score <10):
                    analyzer.collect_data_in_csv_format(md5, mid_scored_hashes)
                 elif (av_score >=10):
                    analyzer.collect_data_in_csv_format(md5, high_scored_hashes)
                 else:
                    print "Total score of Antivirus Engines is "+str(av_score)+" and doesn't meet the minumim requirement!"


