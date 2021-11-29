import pyttsx3
import asyncio
import defaultdict

variables = defaultdict.DefaultDict()
functions = defaultdict.DefaultDict()
ln = 1
lastin = ""
cmp = ""
dataman = "";

async def main():
    name = input("Name of .jint file: ")
    keywords = ["print,", "input,", "getinput,", "say,", "jump,", "cmp,", "if,", "var,", "func,", "call,"]
    x = open(name)
    i = True
    y=0
    errorflag = 0
    while (i):
        a = x.readline()
        if a != "":
            if keywords.__contains__(a.split(" ")[0]):
                pass
            else:
                errorflag = 1
                print(f"ERROR in line {y} '{a}' is not a command")
        else:
            if errorflag != 1:
                x.close()
                i = False
            else:
                print("JINT PROG stopped because of errors")
                return
    with open(name) as f:

        async def dataCheck():
            global ln
            global variables
            global functions
            global dataman
            global lastin
            global cmp
            global functions

            if dataman == "":
                data = f.readline()
            else:
                data = dataman
                dataman = ""

            if data == "":
                print("\nJINT PROG EXIT")
            else:
                #could be donw with string split
                if data.split(" ")[0] == "print,":
                    if data[7] == "$":
                        print(variables[data[8:data.find(";")]])
                    else:
                        print(data[7:data.find(";")])
                    ln +=1;
                    await dataCheck()
                elif data.split(" ")[0] == "say,":
                    engine = pyttsx3.init()
                    if data[5] != "$":
                        engine.say(data[5:data.find(";")])
                    else:
                        engine.say(variables[data[6:data.find(";")]])
                    engine.runAndWait()
                    ln +=1;
                    await dataCheck()
                elif data.split(" ")[0] == "input,":
                    lastin = input(data[7:data.find(";")])
                    ln +=1;
                    await dataCheck()
                elif data.split(" ")[0] == "getinput,":
                    variables[data[10:data.find(";")]] = lastin
                    ln +=1;
                    await dataCheck()
                elif data.split(" ")[0] == "cmp,":
                    if data[5] != "$":
                        cmp=data[5:data.find(";")]
                    else:
                        cmp=variables[data[6:data.find(";")]]
                    ln+=1
                    await dataCheck()
                elif data.split(" ")[0] == "if,":
                    if data[4] != "$":
                        if cmp == data[4:data.find(":")]:
                            if data[4:data.find(";")].__contains__(":"):
                                a = str(functions[data[data.find(":")+1:data.find(";")]])
                                if keywords.__contains__(a.split(" ")[0]):
                                    dataman = a
                                    variables["cmpret"] = "1"
                                else:
                                    print(f"ERROR function has invailid command {a} in line {ln}")
                                    return

                            else:
                                print(f"ERROR please assign an if function using ':' after the condtion in line: {ln}")
                                return
                        else:
                            variables["cmpret"] = "0"
                    else:
                        if cmp == variables[data[5:data.find(":")]]:
                            if data[4:data.find(";")].__contains__(":"):
                                a = str(functions[str(data[data.find(":")+1:data.find(";")])])
                                if keywords.__contains__(a.split(" ")[0]):
                                    dataman = a
                                    variables["cmpret"] = "1"
                                else:
                                    print(f"ERROR function has invailid command {a} in line {ln}")
                                    return
                            else:
                                print(f"ERROR please assign an if function using ':' after the condtion in line: {ln}")
                                return
                        else:
                            variables["cmpret"] = "0"
                    ln+=1
                    await dataCheck()
                elif data.split(" ")[0] == "var,":
                    if data[5:data.find(";")].__contains__("="):
                        if data[6:data.find("=")].__contains__(" "):
                            print(f"ERROR in line: {ln} var defs are not to have spaces")
                        else:
                            variables[data[5:data.find("=")]] = data[data.find("=") + 1: data.find(";")]
                    else:
                        print(f"ERROR please specify a value after variable name using the '=' operator in line: {ln}")
                        return
                    ln+=1
                    await dataCheck()
                elif data.split(" ")[0] == "func,":
                    if data[6:data.find(";")].__contains__("="):
                        if data[6:data.find("=")].__contains__(" "):
                            print(f"ERROR in line: {ln} functions defs are not to have spaces")
                        else:
                            functions[data[6:data.find("=")]] = data[data.find("=") + 1: -1]
                    else:
                        print(f"ERROR please specify a value after variable name using the '=' operator in line: {ln}")
                        return
                    ln+=1
                    await dataCheck()
                elif data.split(" ")[0] == "call,":
                    a = functions[data[6:data.find(";")]]
                    if keywords.__contains__(a.split(" ")[0]):
                        dataman = a
                    else:
                        print(f"ERROR function has invailid command {a} in line {ln}")
                        return
                    ln+=1
                    await dataCheck()

        await dataCheck()
asyncio.run(main())
