CmdChar = "!"

def join_strings(str1, str2):
    return str1 + str2


outputstr = ""

def on_message(message):
    if message.startswith(CmdChar + 'py'):
        global outputstr
        ouputstr = ""

        codedMessage = message.replace(CmdChar + "py", "", 1)  # Remove the command part of the message (!py)
        codedMessage = codedMessage.lstrip()  # Remove all leading whitespace
        codedMessage = codedMessage.replace("print(", "global outputstr \noutputstr += join_strings(outputstr, ")  # Change every print to adding a new line to the collective output, to be sent as a message later.

        print(codedMessage)
        exec(codedMessage)
        print(outputstr)

        # print(outputstr)
        outputstr = outputstr.replace("[EOL]", "\n")

        if (len(outputstr) == 0):
            print("Output was empty!")

        else:
            print(outputstr)


message = '!py print("test")'

on_message(message)
