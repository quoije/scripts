Write-Host "[1] Set hypervisor launch option to auto (Hyper-V)"
Write-Host "[2] Set hypervisor launch option to off (VMWare)"

$a = Read-Host -Prompt "Type your choice"

$systemcheck = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($systemcheck) {
    if ($a -eq 1) {
        Write-Host "[+] doing 'bcdedit /set hypervisorlaunchtype auto' command"
        bcdedit /set hypervisorlaunchtype auto
        $prompt = Read-Host -Prompt "[+} do you want to reboot? (y/n)"
        if ($prompt -eq "y") {
            Write-Host "    [+] rebooting"
            restart-computer -Confirm
        }
    }
    elseif ($a -eq 2) {
        Write-Host "[+] doing 'bcdedit /set hypervisorlaunchtype off' command"
        bcdedit /set hypervisorlaunchtype off
        $prompt = Read-Host -Prompt "[+} do you want to reboot? (y/n)"
        if ($prompt -eq "y") {
            Write-Host "    [+] rebooting"
            restart-computer -Confirm
        }
    }
}
else
{
    Write-Host "[+] not admin :("
}
