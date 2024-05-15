import streamlit as st
import numpy as np
import pandas as pd

st.text_input("y = ", key = "eqn")
st.text_input("x = ", key = "x")

# Convert the eqn to a list of digits and operations.
def str_to_eqn(eqn_str):
  # Expression is a list of digits and operations.
  expression = []
  # Remove whitespace.
  eqn_str = eqn_str.replace(" ", "")
  # Number of left and right parentheses.
  num_left = 0
  num_right = 0
  i = 0
  while (i < len(eqn_str)):
    if (eqn_str[i] == "0"):
      # Add the current digit to the expression.
      expression.append("0")
    elif (eqn_str[i] == "1"):
      expression.append("1")
    elif (eqn_str[i] == "2"):
      expression.append("2")
    elif (eqn_str[i] == "3"):
      expression.append("3")
    elif (eqn_str[i] == "4"):
      expression.append("4")
    elif (eqn_str[i] == "5"):
      expression.append("5")
    elif (eqn_str[i] == "6"):
      expression.append("6")
    elif (eqn_str[i] == "7"):
      expression.append("7")
    elif (eqn_str[i] == "8"):
      expression.append("8")
    elif (eqn_str[i] == "9"):
      expression.append("9")
    elif (eqn_str[i] == "."):
      expression.append(".")
    elif (eqn_str[i] == "("):
      # num_left and right_index are used to see what is inside which pair of parentheses.
      num_left += 1
      right_index = len(eqn_str)
      j = i + 1
      # Iterate until there are the correct number of right parentheses.
      # If the number of right parentheses is equal to the number of left parentheses, then all the parentheses are closed.
      while (num_left != num_right):
        if (eqn_str[j] == ")"):
          num_right += 1
        elif (eqn_str[j] == "("):
          num_left += 1
        j += 1
      right_index = j
      expression.append(str_to_eqn(eqn_str[i + 1:right_index]))
      i = right_index - 1
    elif (eqn_str[i] == "^"):
      expression.append("^")
    elif (eqn_str[i] == "*"):
      expression.append("*")
    elif (eqn_str[i] == "/"):
      expression.append("/")
    elif (eqn_str[i] == "+"):
      expression.append("+")
    elif (eqn_str[i] == "-"):
      expression.append("-")
    elif (eqn_str[i] == "x"):
      expression.append("x")
    i += 1
  return expression

# Evaluate the list of digits and operations.
def evaluate(eqn, x):
  val = 0
  i = 0
  # Preevaluation processing
  while (i < len(eqn)):
    # If it's a list, that means it's inside parentheses, so evaluate the stuff inside the parentheses.
    if (isinstance(eqn[i], list)):
      eqn[i] = evaluate(eqn[i], x)
    elif (eqn[i] == 'x'):
      eqn[i] = x
    elif (eqn[i].isdigit()):
      is_digit = True
      num_of_digits = 1
      while (is_digit and i + num_of_digits < len(eqn)):
        if (ord(list(eqn[i + num_of_digits])[0]) >= 48
            and ord(list(eqn[i + num_of_digits])[0]) <= 57
            or ord(list(eqn[i + num_of_digits])[0]) == 46):
          num_of_digits += 1
        else:
          is_digit = False
      num_str = ""
      for j in range(num_of_digits):
        num_str += eqn[i + j]
      eqn[i] = float(num_str)
      for _ in range(num_of_digits - 1):
        eqn.pop(i + 1)
    i += 1
  # Exponentiation
  i = 0
  while (i < len(eqn)):
    if (eqn[i] == '^'):
      eqn[i - 1] **= eqn[i + 1]
      eqn.pop(i)
      eqn.pop(i)
      i -= 2
    i += 1
  # Multiplication and Division
  i = 0
  while (i < len(eqn)):
    if (eqn[i] == '*'):
      eqn[i - 1] *= eqn[i + 1]
      eqn.pop(i)
      eqn.pop(i)
      i -= 2
    elif (eqn[i] == '/'):
      eqn[i - 1] /= eqn[i + 1]
      eqn.pop(i)
      eqn.pop(i)
      i -= 2
    #elif (isinstance(eqn[i], float) or isinstance(eqn[i], int)) and (isinstance(eqn[i + 1], float) or isinstance(eqn[i + 1], int)):
      #eqn[i] = eqn[i] * eqn[i + 1]
      #eqn.pop(i + 1)
    i += 1
  # Addition and Subtraction
  i = 0
  while (i < len(eqn)):
    if (eqn[i] == '+'):
      eqn[i - 1] += eqn[i + 1]
      eqn.pop(i)
      eqn.pop(i)
      i -= 2
    elif (eqn[i] == '-'):
      eqn[i - 1] -= eqn[i + 1]
      eqn.pop(i)
      eqn.pop(i)
      i -= 2
    i += 1
  val = eqn[0]
  return val

eqn_str = st.session_state.eqn
if (eqn_str):
  eqn_str = str(eqn_str)

x = st.session_state.x
if (x):
  x = float(x)

if (eqn_str and x):
  st.write(evaluate(str_to_eqn(eqn_str), x))
