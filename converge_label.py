#converging files and labeling them all


import json

#i want the set up to be
#jpg
#pub_date
#main_url
#heaadinline
#school
#pdf_url
#txt

create_json = []
 
#file = 'revised_kstate_whoop_pdf.json'
file = 'revised_missu_whoop_pdf.json'
#file = 'revised_osu_whoop_pdf.json'
#file = 'ag_04_whoop_merged.json'
#file = 'wiscon_whoop_pdf.json'


def open_file(file_name):
	with open(file_name, 'r') as f:
		data = json.load(f)
		return data


for key in open_file(file):
	print(key.keys())

	create_json.append(dict(
		{
		"jpg_url" : key['jpg_url'],
		"pub_date" : key['published_date'],
		"sort_date" : 'published_date_iso',
		"main_url" : key['home_url'],
		"school" : 'Missouri Extenstion',
		"pdf_url" : key['pdf_url'],
		"headline" : key['headline'],
		"txt ": key['txt']
		}))
json_data = json.dumps(create_json,indent=4)
with open('missouri_use_me.json','w') as f:
	f.write(json_data)

