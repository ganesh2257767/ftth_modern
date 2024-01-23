import gooeypie as gp
from check_feasibility import *
import threading
import time
from itertools import zip_longest

version = 1.1
headings = ['Address', 'Availablility', 'Port']
loading_flag = False

def setup():
    set_address_dropdown(False)
    set_technology_dropdown(False)


def set_address_dropdown(event):
    if event:
        addresses = DATA[event.widget.selected]["addresses"]
    else:
        addresses = DATA["QA INT"]["addresses"]
    t = []
    for side in ("OPT", "SDL"):
        for lst in addresses[side].values():
            t.extend(lst)
    select_address_dd.items = t


def set_technology_dropdown(event):
    if event:
        if event.event_name == 'change':
            tech = list(DATA[event.widget.selected]["addresses"][side_dd.selected].keys())
        else:
            tech = list(DATA[env_radio_1.selected]["addresses"][event.widget.selected].keys())
    else:
        tech = list(DATA[env_radio_1.selected]["addresses"][side_dd.selected].keys())
    technology_dd.items = tech


def send_request(next=False):
    global loading_flag
    loading_flag = True
    threading.Thread(target=loading, args=(next,), daemon=True).start()
    output_str = ''
    if next:
        feasibility_response = next_available(env_radio_1.selected, technology_dd.selected, side_dd.selected)
        o = output_tb_1
    else:
        feasibility_response = check_feasibility(env_radio.selected, select_address_dd.selected)
        o = output_tb

    if feasibility_response['success']:
        output_str += f"Address: {feasibility_response['address']}\n\nAvailability: {feasibility_response['availability']}\n\nPDO Port: {feasibility_response.get('ftthPdo', 'None')}"
        o.text = output_str
        app.update()
    else:
        output_str += f"Error: {feasibility_response['errorMessage']}"
        o.text = output_str
        app.update()
        app.alert("Error", f"Error: {feasibility_response['errorMessage']}", "error")
    loading_flag = False
    


def loading(next=False):
    # ls = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
    # ls = ["⠁","⠂","⠄","⡀","⡈","⡐","⡠","⣀","⣁","⣂","⣄","⣌","⣔","⣤","⣥","⣦","⣮","⣶","⣷","⣿","⡿","⠿","⢟","⠟","⡛","⠛","⠫","⢋","⠋","⠍","⡉","⠉","⠑","⠡","⢁"]
    ls = [
			"▰▱▱▱▱▱▱ ",
			"▰▰▱▱▱▱▱ ",
			"▰▰▰▱▱▱▱ ",
			"▰▰▰▰▱▱▱ ",
			"▰▰▰▰▰▱▱ ",
			"▰▰▰▰▰▰▱ ",
			"▰▰▰▰▰▰▰ ",
			"▰▱▱▱▱▱▱ "
		]
    global loading_flag
    i = 0
    if next:
        l = loading_lbl_1
        b = submit_btn_1
    else:
        l = loading_lbl
        b = submit_btn
        
    while loading_flag:
        b.disabled = True
        l.text = ls[i%len(ls)]
        app.update()
        time.sleep(0.2)
        i += 1
    l.text = ' '*25
    b.disabled = False


def display_ratecode(event):
    data_table.clear()
    video_table.clear()
    voice_table.clear()
    
    data_bring = rate_codes[corp_radio.selected]["Bring Codes"][technology_radio.selected]
    data_install = rate_codes[corp_radio.selected][proposal_radio.selected]["Install"]
    data_service = rate_codes[corp_radio.selected][proposal_radio.selected]["Services"][technology_radio.selected]
    data_fee = rate_codes[corp_radio.selected][proposal_radio.selected]["Modem Fee"]
    
    data_bring = [f'{k}: {v}' for k, v in data_bring.items()]
    data_install = [f'{k}: {v}' for k, v in data_install.items()]
    data_service = [f'{k}: {v}' for k, v in data_service.items()]
    
    if proposal_radio.selected == 'Residential':
        video_bring = rate_codes[corp_radio.selected][proposal_radio.selected]["Video"]["Bring Codes"]
        video_install = rate_codes[corp_radio.selected][proposal_radio.selected]["Video"]["Install"]
        video_service = rate_codes[corp_radio.selected][proposal_radio.selected]["Video"]["Services"]
        
        video_bring = [f'{k}: {v}' for k, v in video_bring.items()]
        video_service = [f'{k}: {v}' for k, v in video_service.items()]
        
        video_data = list(map(list, zip_longest(video_bring, video_service, [video_install], fillvalue='')))
        video_table.data = video_data
    
    voice_install = rate_codes[corp_radio.selected][proposal_radio.selected]["Voice"]["Install"]
    voice_service = rate_codes[corp_radio.selected][proposal_radio.selected]["Voice"]["Services"]
    
    voice_service = [f'{k}: {v}' for k, v in voice_service.items()]
    
    nef = rate_codes[corp_radio.selected][proposal_radio.selected]["NEF"]
    promo = rate_codes[corp_radio.selected][proposal_radio.selected]["Promo Tracker"]
    
    data_data = list(map(list, zip_longest(data_bring, data_service, data_install, [data_fee], fillvalue='')))
    voice_data = list(map(list, zip_longest(voice_service,[voice_install], [nef], [promo], fillvalue='')))
    
    data_table.data = data_data    
    voice_table.data = voice_data    
        
    ratecode_window.show_on_top()
    

app = gp.GooeyPieApp(f'Check Feasibility v{version}')
app.set_resizable(False)
try:
    app.set_icon('.//favicon.png')
except FileNotFoundError:
    pass


tab_container = gp.TabContainer(app)

# ------------------------ check_feasibility_on_a_specific_address_tab ----------------------------------------
check_feasibility_on_a_specific_address_tab = gp.Tab(tab_container, 'Check Feasibility On A Specific Address')

env_lbl = gp.Label(check_feasibility_on_a_specific_address_tab, 'Select Environment')
env_radio = gp.Radiogroup(check_feasibility_on_a_specific_address_tab, ['QA INT', 'QA 2'], 'horizontal')
env_radio.selected_index = 0
env_radio.add_event_listener('change', set_address_dropdown)


select_address_lbl = gp.Label(check_feasibility_on_a_specific_address_tab, 'Select Address')
select_address_dd = gp.Dropdown(check_feasibility_on_a_specific_address_tab, [])
select_address_dd.width = 40

container = gp.Container(check_feasibility_on_a_specific_address_tab)
submit_btn = gp.Button(container, 'Check', lambda x: threading.Thread(target=send_request).start())
submit_btn.margin_right = 1
loading_lbl = gp.Label(container, ' '*25)
loading_lbl.margin_left = 1

padding = gp.Label(check_feasibility_on_a_specific_address_tab, '')

output_tb = gp.Textbox(check_feasibility_on_a_specific_address_tab, 20, 7)

container.set_grid(1, 2)
container.add(submit_btn, 1, 1, align='left')
container.add(loading_lbl, 1, 2, align='left')

check_feasibility_on_a_specific_address_tab.set_grid(6, 2)
check_feasibility_on_a_specific_address_tab.add(env_lbl, 1, 1)
check_feasibility_on_a_specific_address_tab.add(env_radio, 1, 2)
check_feasibility_on_a_specific_address_tab.add(select_address_lbl, 2, 1)
check_feasibility_on_a_specific_address_tab.add(select_address_dd, 2, 2)
check_feasibility_on_a_specific_address_tab.add(container, 3, 2)
check_feasibility_on_a_specific_address_tab.add(padding, 4, 1)
check_feasibility_on_a_specific_address_tab.add(output_tb, 5, 1, column_span=2, fill=True)

# ------------------------ END check_feasibility_on_a_specific_address_tab ----------------------------------------
# ------------------------ next_available_address_tab ----------------------------------------
next_available_address_tab = gp.Tab(tab_container, 'Next Available Address')
env_lbl_1 = gp.Label(next_available_address_tab, 'Select Environment')
env_radio_1 = gp.Radiogroup(next_available_address_tab, ['QA INT', 'QA 2'], 'horizontal')
env_radio_1.selected_index = 0
env_radio_1.add_event_listener('change', set_technology_dropdown)

side_lbl = gp.Label(next_available_address_tab, 'Select Side')
side_dd = gp.Dropdown(next_available_address_tab, ['OPT', 'SDL'])
side_dd.selected_index = 0
side_dd.add_event_listener('select', set_technology_dropdown)

technology_lbl = gp.Label(next_available_address_tab, 'Select Technology')
technology_dd = gp.Dropdown(next_available_address_tab, [])

container_1 = gp.Container(next_available_address_tab)
submit_btn_1 = gp.Button(container_1, 'Check', lambda x: threading.Thread(target=send_request, args=(True,)).start())
submit_btn_1.margin_right = 1
loading_lbl_1 = gp.Label(container_1, ' '*25)
loading_lbl_1.margin_left = 1

output_tb_1 = gp.Textbox(next_available_address_tab, 20, 7)

container_1.set_grid(1, 2)
container_1.add(submit_btn_1, 1, 1, align='left')
container_1.add(loading_lbl_1, 1, 2, align='left')

next_available_address_tab.set_grid(5, 2)
next_available_address_tab.add(env_lbl_1, 1, 1)
next_available_address_tab.add(env_radio_1, 1, 2)
next_available_address_tab.add(side_lbl, 2, 1)
next_available_address_tab.add(side_dd, 2, 2)
next_available_address_tab.add(technology_lbl, 3, 1)
next_available_address_tab.add(technology_dd, 3, 2)
# next_available_address_tab.add(submit_btn_1, 4, 1, column_span=2, align='center')
next_available_address_tab.add(container_1, 4, 2)
next_available_address_tab.add(output_tb_1, 5, 1, column_span=2, fill=True)

# ------------------------ END next_available_address_tab ----------------------------------------
# ------------------------ START ratecodes_tab ----------------------------------------
ratecodes_tab = gp.Tab(tab_container, 'Ratecodes')

container_2 = gp.Container(ratecodes_tab)

corp_radio = gp.LabelRadiogroup(container_2, 'Corp', ['Optimum', 'Suddenlink'])
corp_radio.selected_index = 0

proposal_radio = gp.LabelRadiogroup(container_2, 'Proposal', ['Residential', 'Commercial'])
proposal_radio.selected_index = 0

technology_radio = gp.LabelRadiogroup(container_2, 'Technology', ['GPON', 'XGSPON'])
technology_radio.selected_index = 0

view_btn = gp.Button(ratecodes_tab, 'View', display_ratecode)

container_2.set_grid(1, 3)

container_2.add(corp_radio, 1, 1)
container_2.add(proposal_radio, 1, 2)
container_2.add(technology_radio, 1, 3)

ratecodes_tab.set_grid(2, 1)
ratecodes_tab.add(container_2, 1, 1, align='center')
ratecodes_tab.add(view_btn, 2, 1, align='center')

tab_container.add(check_feasibility_on_a_specific_address_tab)
tab_container.add(next_available_address_tab)
tab_container.add(ratecodes_tab)

ratecode_window = gp.Window(app, "Ratecodes")
data_table = gp.Table(ratecode_window, ['Data Bring', 'Data Service', 'Data Install', 'Data Fee'])
data_table.set_column_alignments('center', 'center', 'center', 'center')
data_table.height = 5
data_table.sortable = False
video_table = gp.Table(ratecode_window, ['Video Bring', 'Video Service', 'Video Install'])
video_table.set_column_alignments('center', 'center', 'center')
video_table.height = 6
video_table.sortable = False
voice_table = gp.Table(ratecode_window, ['Voice Service', 'Voice Install', 'NEF', 'Tracker'])
voice_table.set_column_alignments('center', 'center', 'center', 'center')
voice_table.height = 4
voice_table.sortable = False

close_btn = gp.Button(ratecode_window, 'Close', lambda x: ratecode_window.hide())

ratecode_window.set_grid(4, 1)
ratecode_window.add(data_table, 1, 1)
ratecode_window.add(video_table, 2, 1, fill=True)
ratecode_window.add(voice_table, 3, 1)
ratecode_window.add(close_btn, 4, 1, align='center')
# ------------------------ END ratecodes_tab ----------------------------------------

app.set_grid(1, 1)
app.add(tab_container, 1, 1)

app.on_open(setup)
app.run()