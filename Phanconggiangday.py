import PySimpleGUI as sg
from Quanlyhocsinh import mydb

mycursor = mydb.cursor()
strat_headings = ['Môn','Giáo_viên_giảng dạy','Lớp_được_dạy']

mycursor.execute('select * from phanconggiangday')
strat =  mycursor.fetchall()
strat_list = []
for i in strat:
    strat_list.append(list(i))
    
strat_lo = [[sg.Text('\tPhân công giảng dạy',justification='center',font = 'Calibra 20')],
              [sg.Table(strat_list,
                        strat_headings,
                        background_color='LightBlue4',justification='center',
                        text_color='white',change_submits=True,
                        enable_click_events=True,
                        k='-STRATTABLE-'),sg.Column([[sg.Button('Nhập',key='-INSERT5-',expand_x=True)],[sg.Button('Sửa',expand_x=True,key='-FIX5-',disabled=True)],[sg.Button('Tìm kiếm',key='-FIND5-')],[sg.Button('Xóa',expand_x=True,disabled=True,key= '-DEL5-')]])],
              [sg.Input(key = '-INFOR5-')],
              [sg.Exit(k='-EXIT6-')]]    

def Nhập(window):
    add_strat = sg.Window('Phân công giáo viên',layout=[[sg.T('Môn:'),sg.In(k='-SUBJ-')],
                                                        [sg.T('Giáo viên phụ trách:'),sg.In(k='-TC-')],
                                                        [sg.T('Lớp được dạy:'),sg.In(k='-CLS-')],
                                                        [sg.Ok('Xác nhận',k = '-OKSTRAT-')]])
    while True:
        choices,values = add_strat.read()
        if choices == sg.WIN_CLOSED:
                break
        if choices == '-OKSTRAT-':
           if values['-SUBJ-'] == '':
               sg.popup('Bạn chưa điền đầy đủ thông tin cần thiết')     
           else:
               mycursor.execute(('insert into phanconggiangday values(%s,%s,%s)'),
                                (values['-SUBJ-'],values['-TC-'],values['-CLS-']))
               sg.popup('Đã thêm thông tin mới')
               strat_list.append([values['-SUBJ-'],values['-TC-'],values['-CLS-']])
               window['-STRATTABLE-'].update(strat_list)
               mydb.commit()
               break
    add_strat.close()
    
def Sửa(window,values,row,column):
    strat_list[row-1][column-1] = values['-INFOR5-']
    sg.popup('Chỉnh sửa thông tin thành công!')
    window['-STRATTABLE-'].update(strat_list)
    mycursor.execute(("update phanconggiangday set {} = %s where Họ_và_tên = %s".format(strat_headings[column-1])),(values['-INFOR5-'],strat_list[row-1][1]))   
    mydb.commit()
    window['-FIX5-'].update(disabled=True)
    
def Tìm_kiếm(window,values):
    strat_search = []   
    for i in range(3):
        for j in range(len(strat_list)):
            if values['-INFOR5-'] in strat_list[j][i]:
                strat_search.append(strat_list[j])
                window['-STRATTABLE-'].update(strat_search)
    if values['-INFOR5-'] == '': window['-STRATTABLE-'].update(strat_list) 

def Xóa(window,row):
    try:
        mycursor.execute('delete from phanconggiangday where Môn = %s',(strat_list[row-1][0],))
        mydb.commit()
        strat_list.remove(strat_list[row-1])
    except:
        print('error')    
    window['-STRATTABLE-'].update(strat_list)
    sg.popup('Xóa thông tin thành công!') 
    window['-DEL5-'].update(disabled = True)     