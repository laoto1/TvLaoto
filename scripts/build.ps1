$env:JAVA_HOME = "C:\Users\Administrator\jdk-17.0.13+11"
& .\gradlew.bat assembleDebug --no-daemon 2>&1 | Select-Object -Last 40

