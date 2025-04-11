import get
import show

dblp = get.DBLP()
data, flag = dblp.get_name('Ya-Qin Zhang')
show = show.show_data()
show.show_dblp(data)