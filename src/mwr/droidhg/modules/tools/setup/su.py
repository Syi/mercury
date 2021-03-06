from mwr.droidhg.modules import common, Module

class MinimalSu(Module, common.SuperUser, common.Shell):

    name = "Prepare 'minimal-su' binary installation on the device."
    description = """Prepares 'minimal-su' binary installation files on the device in order to provide access to a root shell on demand.

This binary provides Mercury the ability to maintain access to a root shell on the device after obtaining a temporary root shell via the use of an exploit. Just type `su` from a shell to get a root shell.

WARNING: This minimal version of the su binary is completely unprotected, meaning that any application on the device can obtain a root shell without any user prompting.
"""
    examples = """
    mercury> run tools.setup.minimalsu
    [*] Uploaded minimal-su
    [*] Uploaded install-minimal-su.sh
    [*] chmod 770 /data/data/com.mwr.droidhg.agent/install-minimal-su.sh
    [*] Ready! Execute /data/data/com.mwr.droidhg.agent/install-minimal-su.sh from root context to install su
    
    ...insert root exploit here...
    u0_a95@android:/data/data/com.mwr.droidhg.agent # /data/data/com.mwr.droidhg.agent/install-minimal-su.sh
    Done. You can now use `su` from a shell.
    u0_a95@android:/data/data/com.mwr.droidhg.agent # exit
    u0_a95@android:/data/data/com.mwr.droidhg.agent $ su
    u0_a95@android:/data/data/com.mwr.droidhg.agent #
    """
    author = "Tyrone (@mwrlabs)"
    date = "2013-04-22"
    license = "MWR Code License"
    path = ["tools", "setup"]

    def execute(self, arguments):
        
        # Check for existence of any su binaries
        if self.isAnySuInstalled():
            self.stdout.write("[!] A version of su is already installed\n")
        
        # Upload su binary
        if self.uploadMinimalSu():
            self.stdout.write("[+] Uploaded minimal-su\n")
        else:
            self.stdout.write("[-] Upload failed (minimal-su) - aborting\n")
            return
        
        # Upload install-minimal-su.sh    
        if self.uploadMinimalSuInstallScript():
            self.stdout.write("[+] Uploaded install-minimal-su.sh\n")
            self.stdout.write("[+] chmod 770 /data/data/com.mwr.droidhg.agent/install-minimal-su.sh\n")
        else:
            self.stdout.write("[-] Upload failed (install-minimal-su.sh) - aborting\n")
            return
        
        # Ready to be used from root context
        self.stdout.write("[+] Ready! Execute /data/data/com.mwr.droidhg.agent/install-minimal-su.sh from root context to install minimal-su\n")

