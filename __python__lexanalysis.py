__key_dictionary = {'False': 101, 'class': 102, 'finally': 103, 'is': 104, 'return': 105, 'None': 106, 'continue': 107,
                    'for': 108, 'lambda': 109, 'try': 110, 'True': 111, 'def': 112, 'from': 113, 'nonlocal': 114,
                    'while': 115, 'and': 116, 'del': 117, 'global': 118, 'not': 119, 'with': 120, 'as': 121,
                    'elif': 122, 'if': 123, 'or': 124, 'yield': 125, 'assert': 126, 'else': 127, 'import': 128,
                    'pass': 129, 'break': 130, 'except': 131, 'in': 132, 'raise': 133,
                    '+': 201, '-': 202, '*': 203, '/': 204, '=': 205, ':': 206, '<': 207, '>': 208, '%': 209, '&': 210,
                    '!': 211, '(': 212, ')': 213, '[': 214, ']': 215, '{': 216, '}': 217, '#': 218, '|': 219, ',': 220,
                    '<=': 221, '>=': 222, '!=': 223, '+=': 224, '-=': 225}  # 存储python中可能出现的关键字的算符等，最后一行不确定用不用加

__signal_list = []  # 使用列表存储分析出的单词
__signal_list_with_num = []  # 存储加上编码的单词
__list_quad = []  # 存储四元式
list_vn = {'E': 0, 'D': 1, 'T': 2, 'G': 3, 'F': 4}
list_vt = {'i': 0, '+': 1, '*': 2, '(': 3, ')': 4}
# 预测分析表
list_E = {'i': 'T D', '(': 'T D'}
list_D = {'+': '+ T D', ')': '', '#': ''}
list_T = {'i': 'F G', '(': 'F G'}
list_G = {'+': '', '*': '* F G', ')': '', '#': ''}
list_F = {'i': 'i', '(': '( E )'}
list_matrix = {'E': list_E, 'D': list_D, 'T': list_T, 'G': list_G, 'F': list_F}

list_vt_1 = {'+': 1, '*': 2, 'i': 3, '(': 4, ')': 5, '#': 6}
# 算符优先关系表
list__1 = {'+': '>', '*': '<', 'i': '<', '(': '<', ')': '>', '#': '>'}
list__2 = {'+': '>', '*': '>', 'i': '<', '(': '<', ')': '>', '#': '>'}
list__3 = {'+': '>', '*': '>', 'i': '', '(': '', ')': '>', '#': '>'}
list__4 = {'+': '<', '*': '<', 'i': '<', '(': '<', ')': '=', '#': ''}
list__5 = {'+': '>', '*': '>', 'i': '', '(': '', ')': '>', '#': '>'}
list__6 = {'+': '<', '*': '<', 'i': '<', '(': '<', ')': '', '#': '='}
list_matrix_1 = {'+': list__1, '*': list__2, 'i': list__3, '(': list__4, ')': list__5, '#': list__6}

__list_var = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L',
              13: 'M', 14: 'N', 15: 'O', 16: 'O', 17: 'Q', 18: 'R', 19: 'S', 20: 'T'}

'''
词法分析可以处理各种语句
语法分析可以处理+ * 和加括号的表达式
语义分析可以处理+ * 的表达式
'''


def __token(__str_0):
    right = 1
    if len(__str_0) == 1:
        __signal_list.append(__str_0[0])
        return __str_0[1:]
    elif __str_0[0].isalpha() or __str_0[0] == '_':
        while __str_0[:right].isidentifier():
            right += 1
        right -= 1
        str_1 = __str_0[:right]
        __signal_list.append(str_1)
        __str_0 = __str_0[right:]
        return __str_0
    elif __str_0[0].isdigit():
        while __str_0[:right].replace('.', '', 1).isdigit():
            right += 1
        right -= 1
        str_1 = __str_0[:right]
        __signal_list.append(str_1)
        __str_0 = __str_0[right:]
        return __str_0
    elif __str_0[0].isspace():
        __str_0 = __str_0[1:]
        return __str_0
    else:
        if __str_0[0] in __key_dictionary:
            if __str_0[:2] in __key_dictionary:
                __signal_list.append(__str_0[:2])
                return __str_0[2:]
            else:
                __signal_list.append(__str_0[0])
                return __str_0[1:]
        else:
            print('出现未定义的字符')
            return __str_0[1:]


def __pretreatment(__str_0):
    __str_0 = ' '.join(__str_0.split())
    while len(__str_0) > 0:
        __str_0 = __token(__str_0)
    return __signal_list


# 以下是两种输出方法


def __print_signal_list(__signal_list):
    for item in __signal_list:
        if item in __key_dictionary:
            __signal_list_with_num.append([item, __key_dictionary[item]])
        else:
            if item[0].isdigit():
                __signal_list_with_num.append([item, 40])
            else:
                __signal_list_with_num.append([item, 39])
    print(__signal_list_with_num)


def __print_signal_list_2(__signal_list):
    for item in __signal_list:
        if item in __key_dictionary:
            __signal_list_with_num.append([__key_dictionary[item], '-'])
        else:
            if item[0].isdigit():
                __signal_list_with_num.append([40, '|'])
            else:
                __signal_list_with_num.append([39, '|'])
    print(__signal_list_with_num)


def __top_to_bottom(signal_list):
    list_stack = ['#', 'E']
    num = 0
    __print(list_stack, signal_list[num:])
    a = signal_list[num]
    flag = True
    while flag:
        x = ''
        if list_stack[0] != '':
            x = list_stack.pop()
        if x in list_vt:
            if x == a:
                num += 1
                a = signal_list[num]
                __print(list_stack, signal_list[num:])
            else:
                print('无法完成匹配操作')
        elif x == '#':
            if x == a:
                print('自上而下语法分析匹配成功')
                flag = False
            else:
                print('栈内为#，栈外非#')
        elif x in list_vn:
            try:
                for i in list_matrix[x][a].split()[::-1]:  # list_matrix['E'] = list_E  list_E['i'] = {T D}
                    list_stack.append(i)
                __print(list_stack, signal_list[num:])
            except KeyError:
                print('在预测分析表中无此产生式')
        else:
            print('error')


def __print(list_stack, list_input):
    print(''.join(list_stack), end='')
    print(''.join(list_input).rjust(30 - len(''.join(list_stack))))


def __bottom_to_top(list_input):
    k = 1
    s = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    s[k] = '#'
    num = -1
    __var_num = 0
    print(''.join(s[1:]), end='')
    print(''.join(list_input[num + 1:]).rjust(30 - len(''.join(s))))
    while True:
        num += 1
        a = list_input[num]
        if s[k] in list_vt_1:
            j = k
        else:
            j = k - 1
        while list_matrix_1[s[j]][a] == '>':
            while True:
                q = s[j]
                if s[j - 1] in list_vt_1:
                    j = j - 1
                else:
                    j = j - 2
                if list_matrix_1[s[j]][q] == '<':  # 书上的这里写错了
                    break
            __var_num += 1
            __var = __list_var[__var_num]
            if k != j + 1 and s[k] != ')':  # 不是把I换成N
                if s[j + 2] == '+':
                    __list_quad.append(['+', s[j + 1], s[k], __var])
                else:
                    __list_quad.append(['*', s[j + 1], s[k], __var])

            _num = len(s)
            while s[j + 1] != '':
                s[_num - 1] = ''
                _num -= 1
            s[j + 1] = __var
            print(''.join(s[1:]), end='')
            print(''.join(list_input[num:]).rjust(30 - len(''.join(s))))
            k = j + 1
        if list_matrix_1[s[j]][a] == '<' or list_matrix_1[s[j]][a] == '=':  # 入栈
            k += 1
            s[k] = a
            print(''.join(s[1:]), end='')
            print(''.join(list_input[num + 1:]).rjust(30 - len(''.join(s))))
        else:
            print('算符优先关系表中无此比较项！')
        if a == '#':
            print('自下而上分析归约成功')
            break


def main():
    _str = 'i+i*i'
    str_0 = 'i+i*i+i'
    str_00 = 'i+i*i*i+i'
    # str_1 = input('请输入想要进行词法分析的字符串：')
    __signal_list_1 = __pretreatment(_str)  # 词法分析的输出结果
    print('词法分析的输入串为：', end='')
    print(''.join(__signal_list_1))
    print('词法分析的结果为:', end='')
    __print_signal_list_2(__signal_list)
    __signal_list_1.append('#')  # 作为语法分析的输入
    print('语法分析的结果为：')
    __top_to_bottom(__signal_list_1)
    __bottom_to_top(__signal_list_1)
    print('四元式：')
    for item in __list_quad:
        print(item)


if __name__ == '__main__':
    main()
