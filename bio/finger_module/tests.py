import pefile

dll_path = r"D:\GrabacionDavid\FDx SDK Pro for Windows v4.3.1_J1.12\FDx SDK Pro for Windows v4.3.1\DotNETFramework\Bin\x64\SecuGen.FDxSDKPro.Windows.dll"

pe = pefile.PE(dll_path)
machine = pe.FILE_HEADER.Machine

if machine == 0x14c:
    print("La DLL es de 32-bit (x86)")
elif machine == 0x8664:
    print("La DLL es de 64-bit (x64)")
else:
    print(f"Arquitectura desconocida: {machine}")
