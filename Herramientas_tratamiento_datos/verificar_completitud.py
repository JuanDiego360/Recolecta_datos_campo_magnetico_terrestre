import pandas as pd

def verificar_completitud(fecha,Num):
	nombre_data=f"CampoMagnetico_{fecha}_{Num}.csv"
	data=pd.read_csv(nombre_data)
	if (Num=="01"):
		if(data.isnull().sum().iloc[2]==0 and len(data)==16335):
			print("datos completos")
			return (True)
		else:
			print(f"datos incompletos, hacen falta {data.isnull().sum().iloc[2]+16335-len(data)} datos.")
			return (False)
	elif(Num=="02"):
		if(data.isnull().sum().iloc[2]==0 and len(data)==16335):
			print("datos completos")
			return (True)
		else:
			print(f"datos incompletos, hacen falta {data.isnull().sum().iloc[2]+16335-len(data)} datos.")
			return (False)
	elif(Num=="03"):
		if(data.isnull().sum().iloc[2]==0 and len(data)==16335):
			print("datos completos")
			return (True)
		else:
			print(f"datos incompletos, hacen falta {data.isnull().sum().iloc[2]+16335-len(data)} datos.")
			return (False)
	elif(Num=="04"):
		if(data.isnull().sum().iloc[2]==0 and len(data)==16336):
			print("datos completos")
			return (True)
		else:
			print(f"datos incompletos, hacen falta {data.isnull().sum().iloc[2]+16336-len(data)} datos.")
			return (False)
resultado=True
for i in ["03"]:
	resultado=resultado and verificar_completitud("2016",i)
	if(not resultado):
		print(f"el data incompleto es el data_{i}")
if (resultado):
	print("datos completos")
else:
	print("datos incompletos")
