$scriptPath = Split-Path -parent $PSCommandPath;
$algoPath = "$scriptPath\run_algo.py"

py -3 $algoPath