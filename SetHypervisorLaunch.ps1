Write-Host "[1] Set hypervisor launch option to auto (Hyper-V)"
Write-Host "[2] Set hypervisor launch option to off (VMWare)"

$a = Read-Host -Prompt "Type your choice"
$hvType = @('auto', 'off')
$selType
$sysCheck = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($sysCheck) {
    if ($a -eq 1) {
        $selType = $hvType[0]
    }
    elseif ($a -eq 2) {
        $selType = $hvType[1]
    }
    if ($selType -eq 'auto' -or $selType -eq 'off')
    {
        Write-Host "[+] doing 'bcdedit /set hypervisorlaunchtype $selType' command"
        bcdedit /set hypervisorlaunchtype $selType 
        $prompt = Read-Host -Prompt "[+] do you want to reboot? (y/n)"
    
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
