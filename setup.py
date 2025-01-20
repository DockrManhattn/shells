import os
import pwd
from pathlib import Path
import subprocess

def get_current_user_and_shell():
    """Get the current user's home directory and shell."""
    home = Path.home()
    user_name = home.parts[-1]
    shell = os.getenv("SHELL", "/bin/sh")
    return user_name, shell

def ensure_local_bin_exists(user_name):
    """Check if /home/{user_name}/.local/bin exists, and create it if it does not."""
    local_bin_path = Path(f"/home/{user_name}/.local/bin")
    if not local_bin_path.exists():
        try:
            local_bin_path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {local_bin_path}")
        except Exception as e:
            print(f"Error creating directory {local_bin_path}: {e}")
    else:
        print(f"Directory already exists: {local_bin_path}")

def copy_shells_script(user_name):
    """Copy shells.py to /home/{user_name}/.local/bin."""
    source_path = Path("shells.py")
    destination_path = Path(f"/home/{user_name}/.local/bin/shells.py")
    try:
        if source_path.exists():
            destination_path.write_bytes(source_path.read_bytes())
            print(f"Copied shells.py to {destination_path}")
        else:
            print(f"Source file shells.py does not exist.")
    except Exception as e:
        print(f"Error copying shells.py to {destination_path}: {e}")

def add_alias_to_shell_rc(user_name, shell):
    """Add an alias to the user's shell configuration file."""
    alias_command = f"alias shells='python3 /home/{user_name}/.local/bin/shells.py'\n"
    if "bash" in shell:
        rc_file = Path(f"/home/{user_name}/.bashrc")
    elif "zsh" in shell:
        rc_file = Path(f"/home/{user_name}/.zshrc")
    else:
        print("Unsupported shell for alias addition.")
        return

    try:
        if rc_file.exists():
            with rc_file.open("a") as file:
                file.write(alias_command)
            print(f"Added alias to {rc_file}")
        else:
            print(f"Shell configuration file {rc_file} does not exist.")
    except Exception as e:
        print(f"Error adding alias to {rc_file}: {e}")

def create_ssl_cert_directory():
    """Create /key directory, set permissions, and generate custom.pem."""
    current_user = pwd.getpwuid(os.getuid()).pw_name
    
    try:
        subprocess.run(["sudo", "mkdir", "-p", "/key"], check=True)
        subprocess.run(["sudo", "chown", f"{current_user}:{current_user}", "/key"], check=True)
        subprocess.run(["sudo", "chmod", "700", "/key"], check=True)
        os.chdir("/key")
        subprocess.run(["sudo", "ls", "-ld", "/key"], check=True)
        
        # Run openssl command with sudo to avoid permission issues
        subprocess.run([
            "sudo", "openssl", "req", "-new", "-x509", "-nodes", 
            "-out", "cert.crt", "-keyout", "priv.key"
        ], check=True)
        
        # Change ownership of generated files to the current user
        subprocess.run(["sudo", "chown", f"{current_user}:{current_user}", "cert.crt", "priv.key"], check=True)
        
        with open("custom.pem", "w") as pem_file:
            with open("priv.key", "r") as priv_key, open("cert.crt", "r") as cert_crt:
                pem_file.write(priv_key.read())
                pem_file.write(cert_crt.read())
                
        print("SSL certificate and key have been created in /key and combined into custom.pem.")
    except Exception as e:
        print(f"Error creating SSL cert and directory: {e}")


if __name__ == "__main__":
    user_name, shell = get_current_user_and_shell()
    print(f"Current user: {user_name}")
    print(f"Current shell: {shell}")
    ensure_local_bin_exists(user_name)
    copy_shells_script(user_name)
    add_alias_to_shell_rc(user_name, shell)
    create_ssl_cert_directory()
