import comtypes.client

powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
print("PowerPoint COM object created successfully")
powerpoint.Quit()