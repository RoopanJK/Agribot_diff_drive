from pyModbusTCP.client import ModbusClient

c = ModbusClient(host="192.168.1.5",port=502,auto_open=True)

try:
    while(1):
        
        check = input("Do you want to check register value(y/n): ")
        if(check=='y'):
            regs = c.read_holding_registers(0,25)
            print("reading")

            if regs:
                print(regs)
            else:
                print("error")
            continue

        addr = int(input("Enter the address: "))
        val = int(input("Enter the value: "))

        c.write_single_register(addr,val)

        regs = c.read_holding_registers(0,25)
        print("reading")

        if regs:
            print(regs)
        else:
            print("error")
except(KeyboardInterrupt):
    quit