def write_red(f, str_):
    f.write('<style="color:#ff0000">%s<>' % str_)


f = open("out.html", "w")
f.write("<html>")

write_red(f, "thing_i_want_to_be_red_in_output")
write_red(f, "thing_i_want_to_be_red_in_output2")
f.write("</html>")
f.close()
