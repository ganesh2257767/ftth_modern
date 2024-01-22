import gooeypie as gp
from check_feasibility import *
import threading

headings = ['Address', 'Availablility', 'Port']

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
    output_str = []
    if next:
        # call next_available
        feasibility_response, *address = next_available(env_radio_1.selected, technology_dd.selected, side_dd.selected)
        o = output_tbl_1
        address = address[0]
    else:
        feasibility_response = check_feasibility(env_radio.selected, select_address_dd.selected)
        o = output_tbl
        address = select_address_dd.selected
    if isinstance(feasibility_response, dict):
        output_str.append([address, feasibility_response['availability'], feasibility_response.get('ftthPdo', 'None')])
        o.data = output_str
        app.update()
    else:
        app.alert("Error", feasibility_response[1], 'error')
        output_str.append(['', feasibility_response[1], ''])
        o.data = output_str
        app.update()
        

app = gp.GooeyPieApp('Test')
app.set_resizable(False)

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

submit_btn = gp.Button(check_feasibility_on_a_specific_address_tab, 'Check', lambda x: threading.Thread(target=send_request).start())

padding = gp.Label(check_feasibility_on_a_specific_address_tab, '')

output_tbl = gp.Table(check_feasibility_on_a_specific_address_tab, headings=headings)
output_tbl.height = 3
output_tbl.set_column_alignments('center', 'center', 'center')
output_tbl.sortable = False

check_feasibility_on_a_specific_address_tab.set_grid(6, 2)
check_feasibility_on_a_specific_address_tab.add(env_lbl, 1, 1)
check_feasibility_on_a_specific_address_tab.add(env_radio, 1, 2)
check_feasibility_on_a_specific_address_tab.add(select_address_lbl, 2, 1)
check_feasibility_on_a_specific_address_tab.add(select_address_dd, 2, 2)
check_feasibility_on_a_specific_address_tab.add(submit_btn, 3, 1, column_span=2, align='center')
check_feasibility_on_a_specific_address_tab.add(padding, 4, 1)
check_feasibility_on_a_specific_address_tab.add(output_tbl, 5, 1, column_span=2, stretch=True, fill=True)

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

submit_btn_1 = gp.Button(next_available_address_tab, 'Check', lambda x: threading.Thread(target=send_request, args=(True,)).start())

output_tbl_1 = gp.Table(next_available_address_tab, headings=headings)
output_tbl_1.height = 3
output_tbl_1.set_column_alignments('center', 'center', 'center')
output_tbl_1.sortable = False


next_available_address_tab.set_grid(5, 2)
next_available_address_tab.add(env_lbl_1, 1, 1)
next_available_address_tab.add(env_radio_1, 1, 2)
next_available_address_tab.add(side_lbl, 2, 1)
next_available_address_tab.add(side_dd, 2, 2)
next_available_address_tab.add(technology_lbl, 3, 1)
next_available_address_tab.add(technology_dd, 3, 2)
next_available_address_tab.add(submit_btn_1, 4, 1, column_span=2, align='center')
next_available_address_tab.add(output_tbl_1, 5, 1, column_span=2, fill=True, stretch=True)

# ------------------------ END next_available_address_tab ----------------------------------------

tab_container.add(check_feasibility_on_a_specific_address_tab)
tab_container.add(next_available_address_tab)

app.set_grid(1, 1)
app.add(tab_container, 1, 1)

app.on_open(setup)
app.run()