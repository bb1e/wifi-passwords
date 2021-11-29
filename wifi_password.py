#libraries
import subprocess #for system commands
import re #for regular expressions

command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
#run command netsh wlan show profiles
#subprocess.run(<line arguments>, <second argument if needed>, <>, ...)
#capture_output -> get the output from the command output & stdout.decode() -> transform the binary data from the output into string

profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
#find all the wifi names (SSID)
#re.findall(regex) -> find all ocurrences  --  after "All User Profile" "(.*)"all til "\r"escape sequence

wifi_list = []
#save wifi names n passwords

#verify if can get password or not
if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = {} #save wifi info

        #see if wifi key absent or not
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        #if absent ignore
        if re.search("Security key           : Absent", profile_info):
            continue
        else:

            wifi_profile["ssid"] = name 

            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            #run key=clear command
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            #capture with regex

            if password == None:
                wifi_profile["password"] = None #some wifi connections dont have password
            else:

                wifi_profile["password"] = password[1]

            wifi_list.append(wifi_profile) #append the information to the list

#show list
for x in range(len(wifi_list)):
    print(wifi_list[x])