# Window PowerShell script

param([string]$workingdirectory)

Set-Location $workingdirectory

Function PythonPathExists {
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = "stop"

    try {
        if(Get-Command python) {
            return $true;
        }
    } catch {
        return $false
    } Finally {
        $ErrorActionPreference=$oldPreference
    }
}

Function TryAddPythonPath {
    $python_path = "$env:LOCALAPPDATA\Programs\Python\Python36"

    if ( (!(PythonPathExists)) -AND (Test-Path "$python_path\python.exe")) {
        Write-host "adding python to path"
        [Environment]::SetEnvironmentVariable("Path", $env:Path + ";$python_path", [EnvironmentVariableTarget]::Machine)

        # Reload environmental variables 
        # https://stackoverflow.com/questions/14381650/how-to-update-windows-powershell-session-environment-variables-from-registry
        foreach($level in "Machine","User") {
           [Environment]::GetEnvironmentVariables($level).GetEnumerator() | % {
              # For Path variables, append the new values, if they're not already in there
              if($_.Name -match 'Path$') { 
                 $_.Value = ($((Get-Content "Env:$($_.Name)") + ";$($_.Value)") -split ';' | Select -unique) -join ';'
              }
              $_
           } | Set-Content -Path { "Env:$($_.Name)" }
        }

    }
}

TryAddPythonPath

if (!(PythonPathExists)) {

    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

    if (Test-Path "$env:PROGRAMFILES (x86)") {
        Write-host "Downloading Python 64-bit installer to py_setup.exe"
        Invoke-WebRequest -OutFile py_setup.exe -Uri "https://www.python.org/ftp/python/3.6.5/python-3.6.5-amd64.exe"
    } else {
        Write-host "Downloading Python 32-bit installer to py_setup.exe"
        Invoke-WebRequest -OutFile py_setup.exe -Uri "https://www.python.org/ftp/python/3.6.5/python-3.6.5.exe"
    }

    Write-host "Running Python setup (script will continue when complete)"
    Start-Process $workingdirectory/"py_setup.exe" -ArgumentList "/quiet" -WorkingDirectory $workingdirectory -wait
    Remove-Item -path "py_setup.exe"

    TryAddPythonPath
} else {
    Write-host "Python already installed"
}

Start-Process python -ArgumentList "scripts/src/setup.py" -WorkingDirectory $workingdirectory -wait -NoNewWindow

# "pause" functionality
#Write-host "Press any key to continue..."
#[void][System.Console]::ReadKey($true)