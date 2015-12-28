#!/usr/bin/python
#
#  [Program]
#
#  CUPP 3.0
#  Common User Passwords Profiler
#
#
#
#  [Author]
#
#  Muris Kurgas aka j0rgan
#  j0rgan [at] remote-exploit [dot] org
#  http://www.remote-exploit.org
#  http://www.azuzi.me
#
#
#
#  [License]
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#  See 'docs/LICENSE' for more information.

import sys
import os
import ConfigParser
import urllib
import gzip
import csv


# Reading configuration file...
config = ConfigParser.ConfigParser()
config.read('cupp.cfg')

years = config.get('years', 'years').split(',')

chars = config.get('specialchars', 'chars').split(',')
dateseparators = config.get('specialchars', 'dateseparators').split(',')

numfrom = config.getint('nums','from')
numto = config.getint('nums','to')

wcfrom = config.getint('nums','wcfrom')
wcto = config.getint('nums','wcto')

threshold = config.getint('nums','threshold')

# 1337 mode configs, well you can add more lines if you add it to config file too.
# You will need to add more lines in two places in cupp.py code as well...
a = config.get('leet','a')
i = config.get('leet','i')
e = config.get('leet','e')
t = config.get('leet','t')
o = config.get('leet','o')
s = config.get('leet','s')
g = config.get('leet','g')
z = config.get('leet','z')


# for concatenations...

def concats(seq, start, stop):
    for mystr in seq:
        for num in xrange(start, stop):
            yield mystr + str(num)


# for sorting and making combinations...

def komb(seq, start):
    for mystr in seq:
        for mystr1 in start:
            yield mystr + mystr1

if len(sys.argv) < 2 or sys.argv[1] == '-h':
	print " ___________ "
	print " \033[07m  cupp.py! \033[27m                # Common"            
	print "      \                     # User"
	print "       \   \033[1;31m,__,\033[1;m             # Passwords" 
	print "        \  \033[1;31m(\033[1;moo\033[1;31m)____\033[1;m         # Profiler"
	print "           \033[1;31m(__)    )\ \033[1;m  "
	print "           \033[1;31m   ||--|| \033[1;m\033[05m*\033[25m\033[1;m      [ Muris Kurgas | j0rgan@remote-exploit.org ]\r\n\r\n"
	
	print "	[ Options ]\r\n"
	print "	-h	You are looking at it baby! :)"
	print " 		 For more help take a look in docs/README"
	print "		 Global configuration file is cupp.cfg\n"	

	print "	-i	Interactive questions for user password profiling\r\n"
	
	print "	-w	Use this option to improve existing dictionary,"
	print "		 or WyD.pl output to make some pwnsauce\r\n"

	print "	-v	Version of the program\r\n"
	exit()

elif sys.argv[1] == '-v':
	print "\r\n	\033[1;31m[ cupp.py ]  v3.0\033[1;m\r\n"
	print "	* Hacked up by j0rgan - j0rgan@remote-exploit.org"
	print "	* http://www.remote-exploit.org\r\n"
	print "	Take a look docs/README file for more info about the program\r\n"
	exit()


elif sys.argv[1] == '-w':
	if len(sys.argv) < 3:
		print "\r\n[Usage]:	"+sys.argv[0]+"  -w  [FILENAME]\r\n"
		exit()
	fajl = open(sys.argv[2], "r")
	listic = fajl.readlines()
	linije = 0
	for line in listic:
		linije += 1
		
	listica = []
	for x in listic:
		listica += x.split()
	
	print "\r\n      *************************************************"	
	print "      *                    \033[1;31mWARNING!!!\033[1;m                 *"
	print "      *         Using large wordlists in some         *"
	print "      *       options bellow is NOT recommended!      *"
	print "      *************************************************\r\n"
	
	conts = raw_input("> Do you want to concatenate all words from wordlist? Y/[N]: ").lower()
	
	
		
	if conts == "y" and linije > threshold:
		print "\r\n[-] Maximum number of words for concatenation is "+str(threshold)
		print "[-] Check configuration file for increasing this number.\r\n"
		print "Info: You try to add "+str(linije)+" lines\r\n"
		conts = raw_input("> Do you want to concatenate all words from wordlist? Y/[N]: ").lower()
	conts = conts
	cont = ['']
	if conts == "y":
		for cont1 in listica:
			for cont2 in listica:
				if listica.index(cont1) != listica.index(cont2):
					cont.append(cont1+cont2)

	spechars = ['']
	spechars1 = raw_input("> Do you want to add special chars at the end of words? Y/[N]: ").lower()
	if spechars1 == "y":
		for spec1 in chars:
			spechars.append(spec1)
			for spec2 in chars:
				spechars.append(spec1+spec2)
				for spec3 in chars:
					spechars.append(spec1+spec2+spec3)
	
	randnum = raw_input("> Do you want to add some random numbers at the end of words? Y/[N]").lower()
	leetmode = raw_input("> Leet mode? (i.e. leet = 1337) Y/[N]: ").lower()

	
	kombinacija1 = list(komb(listica, years))
	kombinacija2 = ['']
	if conts == "y":
		kombinacija2 = list(komb(cont, years))
	kombinacija3 = ['']
	kombinacija4 = ['']
	if spechars1 == "y":
		kombinacija3 = list(komb(listica, spechars))
		if conts == "y":
			kombinacija4 = list(komb(cont, spechars))
	kombinacija5 = ['']
	kombinacija6 = ['']
	if randnum == "y":
		kombinacija5 = list(concats(listica, numfrom, numto))
		if conts == "y":
			kombinacija6 = list(concats(cont, numfrom, numto))
		
	print "\r\n[+] Now making a dictionary..."
	
	print "[+] Sorting list and removing duplicates..."
	
	komb_unique1 = dict.fromkeys(kombinacija1).keys()	
	komb_unique2 = dict.fromkeys(kombinacija2).keys()
	komb_unique3 = dict.fromkeys(kombinacija3).keys()
	komb_unique4 = dict.fromkeys(kombinacija4).keys()
	komb_unique5 = dict.fromkeys(kombinacija5).keys()
	komb_unique6 = dict.fromkeys(kombinacija6).keys()
	komb_unique7 = dict.fromkeys(listica).keys()
	komb_unique8 = dict.fromkeys(cont).keys()
	
	uniqlist = komb_unique1+komb_unique2+komb_unique3+komb_unique4+komb_unique5+komb_unique6+komb_unique7+komb_unique8
	
	unique_lista = dict.fromkeys(uniqlist).keys()
	unique_leet = []
	if leetmode == "y":
		for x in unique_lista: # if you want to add more leet chars, you will need to add more lines in cupp.cfg too...
			x = x.replace('a',a)
			x = x.replace('i',i)
			x = x.replace('e',e)
			x = x.replace('t',t)
			x = x.replace('o',o)
			x = x.replace('s',s)
			x = x.replace('g',g)
			x = x.replace('z',z)
			unique_leet.append(x)
	
	unique_list = unique_lista + unique_leet

	unique_list_finished = []
	for x in unique_list:
		if len(x) > wcfrom and len(x) < wcto:
			unique_list_finished.append(x)

	f = open ( sys.argv[2]+'.cupp.txt', 'w' )
	unique_list_finished.sort()
	f.write (os.linesep.join(unique_list_finished))
	f = open ( sys.argv[2]+'.cupp.txt', 'r' )
	lines = 0
	for line in f:
		lines += 1
	f.close()
	
	
	print "[+] Saving dictionary to \033[1;31m"+sys.argv[2]+".cupp.txt\033[1;m, counting \033[1;31m"+str(lines)+" words.\033[1;m"
	print "[+] Now load your pistolero with \033[1;31m"+sys.argv[2]+".cupp.txt\033[1;m and shoot! Good luck!"
	fajl.close()
	exit()



elif sys.argv[1] == '-i':
	print "\r\n[+] Insert the informations about the victim to make a dictionary"
	print "[+] If you don't know all the info, just hit enter when asked! ;)\r\n"

	# We need some informations first!

	name = raw_input("> Name: ").lower()
	while len(name) == 0 or name == " " or name == "  " or name == "   ":
		print "\r\n[-] You must enter a name at least!"
		name = raw_input("> Name: ").lower()
	name = str(name)

	surname = raw_input("> Surname: ").lower()
	nick = raw_input("> Nickname: ").lower()
	birthdate = raw_input("> Birthdate (DDMMYYYY): ")
	while len(birthdate) != 0 and len(birthdate) != 8:
		print "\r\n[-] You must enter 8 digits for birthday!"
		birthdate = raw_input("> Birthdate (DDMMYYYY): ")
	birthdate = str(birthdate)

	print "\r\n"

	wife = raw_input("> Wife's(husband's) name: ").lower()
	wifen = raw_input("> Wife's(husband's) nickname: ").lower()
	wifeb = raw_input("> Wife's(husband's) birthdate (DDMMYYYY): ")
	while len(wifeb) != 0 and len(wifeb) != 8:
		print "\r\n[-] You must enter 8 digits for birthday!"
		wifeb = raw_input("> Wife's(husband's) birthdate (DDMMYYYY): ")
	wifeb = str(wifeb)
	print "\r\n"

	kid = raw_input("> Child's name: ").lower()
	kidn = raw_input("> Child's nickname: ").lower()
	kidb = raw_input("> Child's birthdate (DDMMYYYY): ")
	while len(kidb) != 0 and len(kidb) != 8:
		print "\r\n[-] You must enter 8 digits for birthday!"
		kidb = raw_input("> Child's birthdate (DDMMYYYY): ")
	kidb = str(kidb)
	print "\r\n"

	pet = raw_input("> Pet's name: ").lower()
	company = raw_input("> Company name: ").lower()
	print "\r\n"

	words = ['']
	oth = raw_input("> Do you want to add some key words about the victim? Y/[N]: ").lower()
	if oth == "y":
		words = raw_input("> Please enter the words, separated by comma. [i.e. hacker, juice, black]: ").lower().split(", ")

	spechars = ['']
	spechars1 = raw_input("> Do you want to add special chars at the end of words? Y/[N]: ").lower()
	if spechars1 == "y":
		for spec1 in chars:
			spechars.append(spec1)
			for spec2 in chars:
				spechars.append(spec1+spec2)
				spechars.append(spec2+spec1)
				for spec3 in chars:
					spechars.append(spec1+spec2+spec3)
					spechars.append(spec1+spec3+spec2)
					spechars.append(spec2+spec1+spec3)
					spechars.append(spec2+spec3+spec1)
					spechars.append(spec3+spec1+spec2)
					spechars.append(spec3+spec2+spec1)

	randnum = raw_input("> Do you want to add some random numbers at the end of words? Y/[N]").lower()
	leetmode = raw_input("> Leet mode? (i.e. leet = 1337) Y/[N]: ").lower()


	print "\r\n[+] Now making a dictionary..."

	# Now me must do some string modifications...

	# Birthdays first
	birthdate_yy = birthdate[-2:]
	birthdate_yyy = birthdate[-3:]
	birthdate_yyyy = birthdate[-4:]
	birthdate_xd = birthdate[1:2]
	birthdate_xm = birthdate[3:4]
	birthdate_dd = birthdate[:2]
	birthdate_mm = birthdate[2:4]

	wifeb_yy = wifeb[-2:]
	wifeb_yyy = wifeb[-3:]
	wifeb_yyyy = wifeb[-4:]
	wifeb_xd = wifeb[1:2]
	wifeb_xm = wifeb[3:4]
	wifeb_dd = wifeb[:2]
	wifeb_mm = wifeb[2:4]

	kidb_yy = kidb[-2:]
	kidb_yyy = kidb[-3:]
	kidb_yyyy = kidb[-4:]
	kidb_xd = kidb[1:2]
	kidb_xm = kidb[3:4]
	kidb_dd = kidb[:2]
	kidb_mm = kidb[2:4]
	
	
	# Convert first letters to uppercase...
	nameup = name.title()
	surnameup = surname.title()
	nickup = nick.title()
	wifeup = wife.title()
	wifenup = wifen.title()
	kidup = kid.title()
	kidnup = kidn.title()
	petup = pet.title()
	companyup = company.title()
	wordsup = []
	for words1 in words:
		wordsup.append(words1.title())
	
	word = words+wordsup
	
	# reverse a name
	rev_name = name[::-1]
	rev_nameup = nameup[::-1]
	rev_nick = nick[::-1]
	rev_nickup = nickup[::-1]
	rev_wife = wife[::-1]
	rev_wifeup = wifeup[::-1]
	rev_kid = kid[::-1]
	rev_kidup = kidup[::-1]
	
	reverse = [rev_name, rev_nameup, rev_nick, rev_nickup, rev_wife, rev_wifeup, rev_kid, rev_kidup]
	rev_n = [rev_name, rev_nameup, rev_nick, rev_nickup]
	rev_w = [rev_wife, rev_wifeup]
	rev_k = [rev_kid, rev_kidup]
	# Let's do some serious work! This will be a mess of code, but... who cares? :)
	
	# Birthdays combinations
	bds = [birthdate_yy, birthdate_yyy, birthdate_yyyy, birthdate_xd, birthdate_xm, birthdate_dd, birthdate_mm]
	
	# add dateseparator combinations
	for ds in dateseparators:
		bds.append(ds)
		
	bdss = []
	
	for bds1 in bds:
		bdss.append(bds1)
		for bds2 in bds:
			if bds.index(bds1) != bds.index(bds2):
				bdss.append(bds1+bds2)
				bdss.append(bds2+bds1)
				for bds3 in bds:
					if bds.index(bds1) != bds.index(bds2) and bds.index(bds2) != bds.index(bds3) and bds.index(bds1) != bds.index(bds3):
						bdss.append(bds1+bds2+bds3)
						bdss.append(bds1+bds3+bds2)
						bdss.append(bds2+bds1+bds3)
						bdss.append(bds2+bds3+bds1)
						bdss.append(bds3+bds1+bds2)
						bdss.append(bds3+bds2+bds1)
							
	# For a woman...
	wbds = [wifeb_yy, wifeb_yyy, wifeb_yyyy, wifeb_xd, wifeb_xm, wifeb_dd, wifeb_mm]
	
	 # add dateseparator combinations
        for ds in dateseparators:
               wbds.append(ds)

	wbdss = []
	
	for wbds1 in wbds:
		wbdss.append(wbds1)
		for wbds2 in wbds:
			if wbds.index(wbds1) != wbds.index(wbds2):
				wbdss.append(wbds1+wbds2)
				wbdss.append(wbds2+wbds1)
				for wbds3 in wbds:
					if wbds.index(wbds1) != wbds.index(wbds2) and wbds.index(wbds2) != wbds.index(wbds3) and wbds.index(wbds1) != wbds.index(wbds3):
						wbdss.append(wbds1+wbds2+wbds3)
						wbdss.append(wbds1+wbds3+wbds2)
						wbdss.append(wbds2+wbds1+wbds3)
						wbdss.append(wbds2+wbds3+wbds1)
						wbdss.append(wbds3+wbds1+wbds2)
						wbdss.append(wbds3+wbds2+wbds1)
						
	# and a child...
	kbds = [kidb_yy, kidb_yyy, kidb_yyyy, kidb_xd, kidb_xm, kidb_dd, kidb_mm]
	
	# add dateseparator combinations
        for ds in dateseparators:
                kbds.append(ds)

	kbdss = []
	
	for kbds1 in kbds:
		kbdss.append(kbds1)
		for kbds2 in kbds:
			if kbds.index(kbds1) != kbds.index(kbds2):
				kbdss.append(kbds1+kbds2)
				kbdss.append(kbds2+kbds1)
				for kbds3 in kbds:
					if kbds.index(kbds1) != kbds.index(kbds2) and kbds.index(kbds2) != kbds.index(kbds3) and kbds.index(kbds1) != kbds.index(kbds3):
						kbdss.append(kbds1+kbds2+kbds3)
						kbdss.append(kbds1+kbds3+kbds2)
						kbdss.append(kbds2+kbds1+kbds3)
						kbdss.append(kbds2+kbds3+kbds1)
						kbdss.append(kbds3+kbds1+kbds2)
						kbdss.append(kbds3+kbds2+kbds1)
	
	# string combinations....
	kombinaac = [pet, petup, company, companyup]
	kombina = [name, surname, nick, nameup, surnameup, nickup]
	kombinaw = [wife, wifen, wifeup, wifenup, surname, surnameup]
	kombinak = [kid, kidn, kidup, kidnup, surname, surnameup]

	kombinaaac = []
	for kombina1 in kombinaac:
		kombinaaac.append(kombina1)
                for kombina2 in kombinaac:
                        if kombinaac.index(kombina1) != kombinaac.index(kombina2) and kombinaac.index(kombina1.title()) != kombinaac.index(kombina2.title()):
                                kombinaaac.append(kombina1+kombina2)
                                kombinaaac.append(kombina2+kombina1)

	kombinaa = []
	for kombina1 in kombina:
		kombinaa.append(kombina1)
		for kombina2 in kombina:
			if kombina.index(kombina1) != kombina.index(kombina2) and kombina.index(kombina1.title()) != kombina.index(kombina2.title()):
				kombinaa.append(kombina1+kombina2)
				kombinaa.append(kombina2+kombina1)

	kombinaaw = []
	for kombina1 in kombinaw:
		kombinaaw.append(kombina1)
		for kombina2 in kombinaw:
			if kombinaw.index(kombina1) != kombinaw.index(kombina2) and kombinaw.index(kombina1.title()) != kombinaw.index(kombina2.title()):
				kombinaaw.append(kombina1+kombina2)
				kombinaaw.append(kombina2+kombina1)
				
	kombinaak = []
	for kombina1 in kombinak:
		kombinaak.append(kombina1)
		for kombina2 in kombinak:
			if kombinak.index(kombina1) != kombinak.index(kombina2) and kombinak.index(kombina1.title()) != kombinak.index(kombina2.title()):
				kombinaak.append(kombina1+kombina2)
				kombinaak.append(kombina2+kombina1)
		
		
	print "\r\n[+] Now combining main person..."
	
	komb1 = list(komb(kombinaa, bdss))
	komb111 = list(komb(kombinaa, wbdss))
	komb112 = list(komb(kombinaa, kbdss))

	print "\r\n[+] Now combining 2nd person..."
	
	komb2 = list(komb(kombinaaw, wbdss))
	komb211 = list(komb(kombinaaw, bdss))
	komb212 = list(komb(kombinaaw, kbdss))

	print "\r\n[+] Now combining kiddy person..."

	komb3 = list(komb(kombinaak, kbdss))
	komb311 = list(komb(kombinaak, bdss))
	komb312 = list(komb(kombinaak, wbdss))

	print "\r\n[+] Now combining pet'n stuff..."
	
	komb4 = list(komb(kombinaa, years))
	komb5 = list(komb(kombinaaac, years))
	komb511 = list(komb(kombinaaac, bdss))
	komb512 = list(komb(kombinaaac, wbdss))
	komb513 = list(komb(kombinaaac, kbdss))
	
	komb6 = list(komb(kombinaaw, years))
	komb7 = list(komb(kombinaak, years))
	
	print "\r\n[+] Now combining words..."

	komb8 = list(komb(word, bdss))
	komb9 = list(komb(word, wbdss))
	komb10 = list(komb(word, kbdss))
	komb11 = list(komb(word, years))
	komb12 = ['']
	komb13 = ['']
	komb14 = ['']
	komb15 = ['']
	komb16 = ['']
	komb21 = ['']
	
	if randnum == "y":
		print "\r\n[+] Now combining with rand numbers..."
		komb12 = list(concats(word, numfrom, numto))
		komb13 = list(concats(kombinaa, numfrom, numto))
		komb14 = list(concats(kombinaaac, numfrom, numto))
		komb15 = list(concats(kombinaaw, numfrom, numto))
		komb16 = list(concats(kombinaak, numfrom, numto))
		komb21 = list(concats(reverse, numfrom, numto))
		
	print "\r\n[+] Now combining reversed stuff..."
	komb17 = list(komb(reverse, years))
	komb18 = list(komb(rev_w, wbdss))
	komb19 = list(komb(rev_k, kbdss))
	komb20 = list(komb(rev_n, bdss))
	komb001 = ['']
	komb002 = ['']
	komb003 = ['']
	komb004 = ['']
	komb005 = ['']
	komb006 = ['']
	if spechars1 == "y":
		print "\r\n[+] Now combining with special chars..."
		komb001 = list(komb(kombinaa, spechars))
		komb002 = list(komb(kombinaaac, spechars))
		komb003 = list(komb(kombinaaw , spechars))
		komb004 = list(komb(kombinaak , spechars))
		komb005 = list(komb(word, spechars))
		komb006 = list(komb(reverse, spechars))
	
	print "[+] Sorting list and removing duplicates, stay a while and listen..."
	
	komb_unique1 = dict.fromkeys(komb1).keys()
	komb_unique111 = dict.fromkeys(komb111).keys()
	komb_unique112 = dict.fromkeys(komb112).keys()

	komb_unique2 = dict.fromkeys(komb2).keys()
	komb_unique211 = dict.fromkeys(komb211).keys()
	komb_unique212 = dict.fromkeys(komb212).keys()

	komb_unique3 = dict.fromkeys(komb3).keys()
	komb_unique311 = dict.fromkeys(komb311).keys()
	komb_unique312 = dict.fromkeys(komb312).keys()

	komb_unique4 = dict.fromkeys(komb4).keys()
	komb_unique5 = dict.fromkeys(komb5).keys()
	komb_unique511 = dict.fromkeys(komb511).keys()
	komb_unique512 = dict.fromkeys(komb512).keys()
	komb_unique513 = dict.fromkeys(komb513).keys()

	komb_unique6 = dict.fromkeys(komb6).keys()
	komb_unique7 = dict.fromkeys(komb7).keys()
	komb_unique8 = dict.fromkeys(komb8).keys()
	komb_unique9 = dict.fromkeys(komb9).keys()
	komb_unique10 = dict.fromkeys(komb10).keys()
	komb_unique11 = dict.fromkeys(komb11).keys()
	komb_unique12 = dict.fromkeys(komb12).keys()
	komb_unique13 = dict.fromkeys(komb13).keys()
	komb_unique14 = dict.fromkeys(komb14).keys()
	komb_unique15 = dict.fromkeys(komb15).keys()
	komb_unique16 = dict.fromkeys(komb16).keys()
	komb_unique17 = dict.fromkeys(komb17).keys()
	komb_unique18 = dict.fromkeys(komb18).keys()
	komb_unique19 = dict.fromkeys(komb19).keys()
	komb_unique20 = dict.fromkeys(komb20).keys()
	komb_unique21 = dict.fromkeys(komb21).keys()
	komb_unique01 = dict.fromkeys(kombinaa).keys()
	komb_unique02 = dict.fromkeys(kombinaac).keys()
	komb_unique03 = dict.fromkeys(kombinaaw).keys()
	komb_unique04 = dict.fromkeys(kombinaak).keys()
	komb_unique05 = dict.fromkeys(word).keys()
	komb_unique07 = dict.fromkeys(komb001).keys()
	komb_unique08 = dict.fromkeys(komb002).keys()
	komb_unique09 = dict.fromkeys(komb003).keys()
	komb_unique010 = dict.fromkeys(komb004).keys()
	komb_unique011 = dict.fromkeys(komb005).keys()
	komb_unique012 = dict.fromkeys(komb006).keys()
	
	uniqlist = bdss+wbdss+kbdss+reverse+komb_unique01+komb_unique02+komb_unique03+komb_unique04+komb_unique05+komb_unique1+komb_unique111+komb_unique112+komb_unique2+komb_unique211+komb_unique212+komb_unique3+komb_unique311+komb_unique312+komb_unique4+komb_unique5+komb_unique511+komb_unique512+komb_unique513+komb_unique6+komb_unique7+komb_unique8+komb_unique9+komb_unique10+komb_unique11+komb_unique12+komb_unique13+komb_unique14+komb_unique15+komb_unique16+komb_unique17+komb_unique18+komb_unique19+komb_unique20+komb_unique21+komb_unique07+komb_unique08+komb_unique09+komb_unique010+komb_unique011+komb_unique012
	
	unique_lista = dict.fromkeys(uniqlist).keys()
	unique_leet = []
	if leetmode == "y":
		for x in unique_lista: # if you want to add more leet chars, you will need to add more lines in cupp.cfg too...
			x = x.replace('a',a)
			x = x.replace('i',i)
			x = x.replace('e',e)
			x = x.replace('t',t)
			x = x.replace('o',o)
			x = x.replace('s',s)
			x = x.replace('g',g)
			x = x.replace('z',z)
			unique_leet.append(x)
	
	unique_list = unique_lista + unique_leet
	
	unique_list_finished = []
	for x in unique_list:
		if len(x) > wcfrom and len(x) < wcto:
			unique_list_finished.append(x)

	unique_list_finished.sort()
	f = open ( name+'.txt', 'w' )
	f.write (os.linesep.join(unique_list_finished))
	f = open ( name+'.txt', 'r' )
	lines = 0
	for line in f:
		lines += 1
	f.close()
	
	print "[+] Saving dictionary to \033[1;31m"+name+".txt\033[1;m, counting \033[1;31m"+str(lines)+"\033[1;m words."
	print "[+] Now load your pistolero with \033[1;31m"+name+".txt\033[1;m and shoot! Good luck!"
	exit()

else:
	print "\r\n[Usage]:	"+sys.argv[0] +"  [OPTIONS] \r\n"
	print "[Help]:		"+sys.argv[0] +"  -h\r\n"
	exit()
