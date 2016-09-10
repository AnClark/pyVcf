#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf8")

import csv
import codecs

class CardClass:
    N="";
    FN="";
    TEL="";
    OTHER = "";
    def __init__(self):
        pass;
    def __del__(self):
        pass;
    def toCsvLine(self):
        return self.N+ "," + self.FN + "," + self.TEL + "," + self.OTHER;
		
		
def extract_decode_HexString_From_N(N):
	N_split = N.split(';');
	name_hex_strings = []
	name_utf8_strings = [];
	
	for item in N_split:
		if item.startswith('='):
			raw_vcf_hexstring = item;
			raw_vcf_hexstring = raw_vcf_hexstring.replace('=', '');
			hex_string = raw_vcf_hexstring.decode('hex');
			
			name_hex_strings.append(hex_string);
			
	for hex_string in name_hex_strings:
		name_utf8_strings.append(unicode(hex_string))
	
	return name_utf8_strings;
	
def extract_decode_HexString_From_FN(FN):
		
	raw_vcf_hexstring = FN.split(':')[1];
	raw_vcf_hexstring = raw_vcf_hexstring.replace('=', '');
	hex_string = raw_vcf_hexstring.decode('hex');
	
	name_utf8_string = unicode(hex_string);
	
	return name_utf8_string;
	
	
def cardParse(cardstr):
    c = CardClass();
    lines = cardstr.split("\n");
    for line in lines:
        if line:
            if line.startswith("N;"):
                N = line[2:];
                names = extract_decode_HexString_From_N(N);
                for name in names:
                    c.N = c.N + name + ",";
                continue;
            if line.startswith("FN;"):
                FN = line[3:];
                name = extract_decode_HexString_From_FN(FN);
                c.FN = name;
                continue;
            if line.startswith("TEL;"):
                c.TEL += line[4:] + ",";
                continue;
            #c.OTHER += line + "\n";
    return c;

if __name__ == "__main__":
    if len(sys.argv) == 2:
        f = open(sys.argv[1], "r");
        fw = open(sys.argv[1]+".csv", "w");
        fw.write(codecs.BOM_UTF8);
        linecount = 0;
        cardcount = 0;
        cardstr = "";
        while True:
            line = f.readline();
            if line:
                #utf8解码
                if line[:3] == codecs.BOM_UTF8:
                    line = line[3:];
                #line = line.decode("utf-8");
                if line.startswith("BEGIN:VCARD"):
                    cardstr = "";
                else:
                    if line.startswith("END:VCARD"):
                        card = cardParse(cardstr);
                        csvline = card.toCsvLine();
                        cardcount += 1;
                        print str(cardcount) + " " + csvline.decode("utf-8")
                        fw.write(csvline+"\n");
                        cardstr = "";
                    else:
                        line = line.replace("\r", "");
                        line = line.replace("\n", "");
                        cardstr = cardstr + line + "\n";
                linecount += 1;
            else:
                break;
        fw.close();
        f.close();
        print sys.argv[1] + " ok, " + str(cardcount) + "records";
    else:
        print "vcf2csv xxx.vcf";
