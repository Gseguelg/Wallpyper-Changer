#
# Collect data
$PYTHON_PATH = $(where.exe pythonw.exe)
$WALLPYPER_MAIN = "$pwd\Python\wallpyper.py"
# get current user SID
$SID_RAW = whoami /user /FO list | findstr SID
$SID = ($SID_RAW -split ' ')[-1]
# user name
$USR_NAME = $env:UserName
$FULL_USR_NAME = "$env:ComputerName\$USR_NAME"
# datetime string
$dt = Get-Date -Format "yyyy-MM-ddTHH:mm:ss.fffffff"
$TASK_NAME = "Wallpyper"
$TASK_PATH = "\$TASK_NAME"
$FULL_TASK_NAME = "$TASK_NAME" + "_task.xml"

#
# Replace collected variables on base.xml task file
$XML_TASK = Get-Content -Path "SchTasks\base_task.xml"  # read base file
$XML_TASK = $XML_TASK -replace "__DATETIME__", $dt
$XML_TASK = $XML_TASK -replace "__FULL_USR_NAME__", $FULL_USR_NAME
$XML_TASK = $XML_TASK -replace "__SID__", $SID
$XML_TASK = $XML_TASK -replace "__EXECUTABLE_CMD__", $PYTHON_PATH
$XML_TASK = $XML_TASK -replace "__CMD_ARGUMENTS__", $WALLPYPER_MAIN
$XML_TASK = $XML_TASK -replace "__CMD_WORKING_DIRECTORY__", "$pwd\Python"
$XML_TASK = $XML_TASK -replace "__TASK_NAME__", $TASK_PATH

#
# create temporal file
Set-Content -Path $FULL_TASK_NAME -Value $XML_TASK  # write modified file

ECHO "Import new file '$FULL_TASK_NAME' into task manager and accept to finish."
pause