
def linear_fit(file_name):
    """
    submitted on Thu Fab 7
    @author: Asaf Harpaz id: 206016248

    this program will accept a file, either in columns form or row form,
    it will extracts the (x, dx, y, dy) data points and the desired graph titles.
    then, using the extracted data,the program will create and save a graph of
    the linear-fit function and data points. using the linear-fit equations, the
    program will print the parameters (a, da, b, db) and the corresponding chi
    and chi-reduced values.
    """
    # first we'll determine the type of data file (columns or rows),
    foo = cols_or_rows(file_name)

    # depending on which file was entered the program will call on a corresponding handling function
    # which will return a dic with the content of the file
    if foo:
        V_dic = rows_handling(file_name)
    elif not foo:
        V_dic = cols_handling(file_name)

    # the program will now check if all data sets match and if all uncertainties are positive.
    foo_2 = check_1(V_dic)

    # if the the data is good to use the program will keep running.
    if foo_2:
        # using the dic from the handling functions we'll calculate the linear fit coefficients.
        ab_values = find_ab(V_dic)

        # using the coefficients and the dic, we'll calculate the chi-squared value.
        chi_squared(V_dic, ab_values)

        # using the coefficients and the dic again, we'll graph the function.
        graph(V_dic, ab_values)

    elif type(foo_2) == str:
        print(foo_2)




def rows_handling(file_name):
    """"" this function will open the new file in 'r' method (after we already removed any tabs from excel).
    it will return a dic with the values of (x, dx, y, dy), the length of the data set and the axis titles."""

    file_pointer = open(file_name, 'r')
    data = file_pointer.read()
    file_pointer.close()

    # we'll make two copies of the data.
    # using one data set to get information on the file and the other to make the dic.
    data2 = data

    # making a list of lines from the data
    data2 = data2.splitlines()

    # using caseload method to make handling easier (this is why we have 2 copies of the data).
    # then making the data into a list of lines.
    data = data.casefold()
    data = data.splitlines()
    file_pointer.close()

    # defining the dic that will be return to the main function
    # 'a1' and 'b1' are values that'll be use in the function - search_best_parameter(filename)
    rows_dic = {'x': [], 'dx': [], 'y': [], 'dy': [], 'a_list': [], 'b_list': []}

    def append_1(f_str, w_line):
        # this inside function accepts the iterated line and a string.
        # using the string which correspond to a key this function will append the line contents to the dic.

        for i in w_line.split(' ')[1:]:
            # sometimes there are still string characters in the line. we don't want to append those.
            # this is why we'll use the try and except method.
            try:
                rows_dic[f_str].append(float(i))
            except ValueError:
                continue

    # now iterating through the data line-list we'll append the data to the dic.
    for line in data:

        # we'll check what what line of data we are dealing with and then append to the right dic key.

        if line.startswith('x'):
            if line.startswith('x axis'):

                # using the index from the line in the first data set we use data2 to add to our dic.
                rows_dic["".join(data2[data.index(line)].split(' ')[0:2])] = " ".join(
                    data2[data.index(line)].split(' ')[2:])

            else:
                append_1('x', line)

        if line.startswith('y'):
            if line.startswith('y axis'):

                # using the index from the line in the first data set we use data2 to add to our dic.
                rows_dic["".join(data2[data.index(line)].split(' ')[0:2])] = " ".join(
                    data2[data.index(line)].split(' ')[2:])

            else:
                append_1('y', line)

        if line.startswith('dx'):
            append_1('dx', line)

        if line.startswith('dy'):
            append_1('dy', line)

        # this next part will be used in the search_best_parameter(filename) function
        if line.startswith('a'):
            append_1('a_list', line)
        if line.startswith('b'):
            append_1('b_list', line)



    # adding the data set length value to the dic. it will be usefull later.
    Tlen = len(rows_dic['x'])
    rows_dic['Tlen'] = Tlen


    return rows_dic


def check_1(V_dic):
    """this inside function accepts the dic from either cols_handling or rows_handling
    it prints and error and returns False if the data set lenght dont match or if the uncertenties are negative.
    it will retrun True otherwise"""

    Tlen = V_dic['Tlen']
    if len(V_dic['y']) != Tlen or len(V_dic['dx']) != Tlen or len(V_dic['dy']) != Tlen:
        return "Input file error: Data lists are not the same length."

    # checking if all uncertainties are positive
    for d in V_dic['dx']:
        if float(d) <= 0:
            return "Input file error: Not all uncertainties are positive."

    for d in V_dic['dy']:
        if float(d) <= 0:
            return "Input file error: Not all uncertainties are positive."

    else:
        return True



def cols_handling(file_name):  # notice the input - "file_name"
    """"" this function will open the new file in 'r' method (after we already removed any tabs from excel).
    it will return a dic with the values of (x, dx, y, dy), the length of the data set and the axis titles."""

    file_pointer = open(file_name, 'r')
    data = file_pointer.read()
    file_pointer.close()

    # we'll make two copies of the data.
    # casfolding one data set to make handling easier
    data2 = data
    data2 = data2.splitlines()
    data = data.casefold()
    data = data.splitlines()

    # creating a list of the columns titles.
    d_names = data[0].split(' ')

    # using the above list we'll make a new dic with corresponding keys.
    cols_dic = {d_names[0]: [], d_names[1]: [], d_names[2]: [], d_names[3]: []}

    # we'll now iterate through the line-list (from the second line onward), appending flouts to our dic.
    # we'll keep doing that until getting an error, meaning we have reached the graph axis titles part
    # using the index of the error we now know from which line we should take the axis titles.
    for line in data[1:]:
        try:
            float(line[0])
            line = line.split(' ')
            for i in range(len(line)):
                try:
                    cols_dic[d_names[i]].append(float(line[i]))
                except ValueError:
                    continue

        except ValueError:
            stoped = data.index(line)
            break
        except IndexError:
            stoped = data.index(line) + 1

            break

    # using the index of the error, we now know from where to take the axis titles.
    # we'll take them from data2 which wasn't casefolded.
    for line2 in data2[stoped:]:
        line2 = line2.split(' ')
        cols_dic["".join(line2[0:2])] = " ".join(line2[2:])

    # adding the data set length value to the dic. it will be usefull later.
    Tlen = len(cols_dic['x'])
    cols_dic['Tlen'] = Tlen

    return cols_dic



def cols_or_rows(file_name):
    """the cols_or_rows open the file with (R+) method.
       it will read the content, then strip 'tabs' that might be there from pasting data from excel.
       then the function will replace the old content with the new one.
       the function determine what type of data was enterd by 'try' method.
       meaning it will try making the letters into a floats (after removing the spaces)
       if there's no error it will call cols_handling else it will call rows_handling."""

    file_pointer = open(file_name, 'r+')
    data = file_pointer.read()
    data = data.replace('\t', ' ')  # removing any tabs left from excel
    file_pointer.seek(0)
    file_pointer.truncate()  # removing original data
    file_pointer.seek(0)
    file_pointer.write(data)  # writing new data without tabs
    file_pointer.close()
    data = data.casefold()  # changing all letters to lowercase so it'll be easier to handel
    data = data.splitlines()  # splitting the text into a list of lines

    f_line = data[0].split(' ')  # looking at the first line without spaces

    # the program checks if there are any numbers in the first line of the text.
    # the program tries to make any character in the first line into float.
    # its success or failure in doing so will tell us which type of file was entered.
    # the program returns True or False depending on which type.
    for n in f_line:
        try:
            float(n)
            return True
        except ValueError:
            continue
    return False


def find_ab(V_dic):
    """"" this function accepts a dic and returns the coefficients values of the linear fit in list form.
     the values are calculated using the equations (4) (5) and (6) from:
     https://moodle.tau.ac.il/pluginfile.php/432758/mod_resource/content/1/Projectinstructions.pdf
     which is located in the second page,
    (to access the file you'll need to log into Tel-aviv university account)."""

    sum_1 = 0  # sum of 1/dy
    sum_2 = 0  # sum of xy/dy
    sum_3 = 0  # sum of x/dy
    sum_4 = 0  # sum of y/dy
    sum_5 = 0  # sum of x^2/dy
    d_len = V_dic['Tlen']  # length of data set

    for i in range(d_len):
        """iterating through the dic values and calculating all of the variable in equations (4) and (5).
        the variables are calculated using equation (6)"""
        sum_1 += (1 / ((V_dic['dy'][i]) * (V_dic['dy'][i])))
        sum_2 += ((V_dic['x'][i] * V_dic['y'][i]) / ((V_dic['dy'][i]) * (V_dic['dy'][i])))
        sum_3 += ((V_dic['x'][i]) / ((V_dic['dy'][i]) * (V_dic['dy'][i])))
        sum_4 += ((V_dic['y'][i]) / ((V_dic['dy'][i]) * (V_dic['dy'][i])))
        sum_5 += (((V_dic['x'][i]) * (V_dic['x'][i])) / ((V_dic['dy'][i]) * (V_dic['dy'][i])))

    # this is equation (4)
    a = (((sum_2 / sum_1) - ((sum_3 / sum_1) * (sum_4 / sum_1))) / (
            (sum_5 / sum_1) - ((sum_3 / sum_1) * (sum_3 / sum_1))))
    da_s = ((1 / (sum_1 * ((sum_5 / sum_1 - (
            (sum_3 / sum_1) * (sum_3 / sum_1))))))) ** .5

    # this is equation (5)
    b = sum_4 / sum_1 - a * sum_3 / sum_1
    db_s = (((da_s) * (da_s)) * ((sum_5)) * (1 / sum_1)) ** (.5)

    return [a, b, da_s, db_s]


def chi_squared(V_dic, ab_value):
    """"" this function accepts a dic type and a list.
    it will extract the variables from the list (those are the linear fit coefficients),
    then while using the values from the dic (x, dx, y, dy), it will calculate the chi and chi reduced of the linear-fit.
    the program calculates this using equation (3) and (7) from:
    https://moodle.tau.ac.il/pluginfile.php/432758/mod_resource/content/1/Projectinstructions.pdf
    which is located in the second page,
    (to access the file you'll need to log into Tel-aviv university account)."""

    a = ab_value[0]
    b = ab_value[1]
    da = ab_value[2]
    db = ab_value[3]
    chi = 0
    Tlen = V_dic['Tlen'] # this is the data set length

    for i in range(Tlen):
        chi += ((V_dic['y'][i] - (a * V_dic['x'][i] + b)) / (V_dic['dy'][i])) ** 2

    if Tlen >= 3:
        chi_red = (chi / (Tlen - 2))
        print('a = ' + str(a) + ' +- ' + str(da))
        print('b = ' + str(b) + ' +- ' + str(db))
        print("chi2 = " + str(chi))
        print("chi2_reduced = " + str(chi_red))

    # we cant calculate chi reduces for a smaller then 2 data set
    elif Tlen <= 3:
        print('a = ' + str(a) + ' +- ' + str(da))
        print('b = ' + str(b) + ' +- ' + str(db))
        print("chi2 = " + str(chi))
        print("Chi reduced can't be calculated for less then two input values")


def graph(V_dic, ab_value):
    """"" this function accepts a dic type and a list.
    it will extract the "a" and "b" variables from the list (those are the linear fit coefficients),
    then import the plotting packages and use those variables to plot a graph.
    it will extract the axis title from the dic and put theme in the graph as well.
    finally the function will save the figure under the name 'linear_fit.svg'. """

    a = ab_value[0]
    b = ab_value[1]

    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(min(V_dic['x']), max(V_dic['x']))

    linear_fit = plt.plot(x, a * x + b, linestyle='-', )
    plt.setp(linear_fit, color='r', linewidth=0.7)
    plt.errorbar(V_dic['x'], V_dic['y'], V_dic['dy'], V_dic['dx'], fmt='none', ecolor='blue')

    # because there are two types of possible dictionaries there -
    # are two possible keys to the y and x titles
    try:
        plt.ylabel(V_dic['yaxis:'])
    except KeyError:
        plt.ylabel('Y axis')
    try:
        plt.xlabel(V_dic['xaxis:'])
    except KeyError:
        plt.xlabel('X axis')

    plt.savefig('linear_fit.svg', dpi=None, facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format='svg',
                transparent=False, bbox_inches=None, pad_inches=0.1,
                frameon=None, metadata=None)
    plt.show()


