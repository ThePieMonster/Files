<#
.SYNOPSIS
  Parses the Visual Studio Subscription Keys Export XML File

.DESCRIPTION
  Outputs a CSV file in the same directory as the XML file.

.PARAMETER XMLFile
  Specifies the KeysExport.xml file path.

.EXAMPLE
  PS> Visual_Studio_Subscription_Keys_Export_XML_Parser -XMLFile "Path"
#>

param(
    [Parameter(Mandatory=$true)]
    [String] $XMLFile
)
$ErrorActionPreference = "Stop"


# Get XML file data
[xml]$xmlAttr = Get-Content -Path $XMLFile

# Find XML keys
$xml1 = $xmlAttr.root.YourKey.Product_Key

# Initialize array
$csvArray = @()

# Loop through each item in XML
foreach($item in $xml1) {
    $name = $item.Name
    $key = $item.Key.'#text'
    
    # Re-write keys that have more than one key
    Try {
        $keyType = $key.GetType()
        if($keyType.BaseType.Name -eq "Array") {
            foreach($k in $key) {
                $csvItemObject = $null
                $csvItemObject = New-Object PSObject
                $csvItemObject | Add-Member -MemberType NoteProperty -Name "Name" -Value $name
                $csvItemObject | Add-Member -MemberType NoteProperty -Name "Key" -Value $k
                $csvArray += $csvItemObject
            }
        } else {
            $csvItemObject = $null
            $csvItemObject = New-Object PSObject
            $csvItemObject | Add-Member -MemberType NoteProperty -Name "Name" -Value $name
            $csvItemObject | Add-Member -MemberType NoteProperty -Name "Key" -Value $key
            $csvArray += $csvItemObject
        }
        #if($name -like "*Windows 11*") { Write-Host $name "-" $key ; pause }
    }
    Catch {
        $exception = $_.Exception
        
        if ($exception -like "*You cannot call a method on a null-valued expression*") {
            Write-Host "Key was not found:" $name
        } else {
            Write-Error "$exception"
        }
    }
}

# Remove duplicates
$csvArray2 = $csvArray | Sort-Object -Property Name,Key -Unique

# Export CSV
$exportPath = $XMLFile.Replace("\KeysExport.xml","\KeysExport.csv")
$csvArray2 | Select-Object -Property Name,Key | Export-Csv -Path $exportPath -NoTypeInformation
Write-Host "File exported to $exportPath"
