# *Mobile Error Log Analyzer*

### **About:** 
Android Debug Bridge (ADB) gathers huge un-neceesary amount of data during logging which results in a large text file.
To reduce redundant data, Mobile Error Log Analyzer gets those same logs from connected device and filters them in an effictive way that does not remove any useful information.

### **How To:** 
1. Connect an Android device and enable USB Debugging.
2. Go to Options -> New. (Not required if first time)
3. Click on Start.
4. Reproduce issue in connected device and then immediately click on Stop.
5. Click on Analyze to filter shown data.
6. Copy entire text or Click on Save to store filter data.

### **How To If ADB Logs Are Already Collected:** 
1. Go to Options -> Open and select that file.
2. Click on Analyze to filter shown data.
3. Copy entire text or Click on Save to store filter data.

For simplicity converted python file into an application. [Mobile Error Log Analyzer.7z](https://github.com/KarthikBH/Mobile_Error_Log_Analyzer/releases/download/0.01/Mobile.Error.Log.Analyzer.7z)
