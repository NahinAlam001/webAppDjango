import json
import sys


json_file = open(sys.argv[1])
data = json.load(json_file)

with open("out.raw", mode="w") as out_file:
    out_file.write(str(0))
    out_file.write(",")
    out_file.write(str(100.00))
    out_file.write(",")
    out_file.write(str(33))

    out_file.write(",")
    out_file.write(str(0))
    out_file.write(",")
    out_file.write(str(1))
    out_file.write(",")
    out_file.write(str(60.00))

    out_file.writelines("\n")
    out_file.writelines("\n")
    out_file.writelines("IEEE 14 BUS TEST CASE \n")

    for record in data:
        # each record is now a python object
        if (
            record["type"] == "bus-data"
            and (record["name"].split()[0]).lower() == "bus"
        ):
            out_file.write(record["name"].split()[1])
            out_file.write(",")
            out_file.write("'" + record["name"] + "'")
            out_file.write(",")
            out_file.write(record["base_kv"])
            out_file.write(",")
            out_file.write(record["code"])
            out_file.write(",")
            out_file.write(record["area_num"])
            out_file.write(",")
            out_file.write(record["zone_num"])
            out_file.write(",")
            out_file.write(record["owner_num"])
            out_file.write(",")
            out_file.write(record["voltage"])
            out_file.write(",")
            out_file.write(record["angle"])
            out_file.write(",")
            out_file.write(record["normal_vmax"])
            out_file.write(",")
            out_file.write(record["normal_vmin"])
            out_file.write(",")
            out_file.write(record["emergency_vmax"])
            out_file.write(",")
            out_file.write(record["emergency_vmin"])

            out_file.write("\n")
    out_file.write("0 \n")  # End Bus data, Begin Load

    for record in data:
        # each record is now a python object
        if (
            record["type"] == "load-data"
            and (record["name"].split()[0]).lower() == "load"
        ):
            out_file.write(record["bus_number"])
            out_file.write(",")
            out_file.write("'" + record["load_id"] + "'")  
            out_file.write(",")
            out_file.write(str(int(record["in_service"])))
            # out_file.write(record["in_service"])  
            out_file.write(",")
            out_file.write(record["area_num"])
            out_file.write(",")
            out_file.write(record["zone_num"])
            out_file.write(",")
            out_file.write(record["Pload_MW"])
            out_file.write(",")
            out_file.write(record["Qload_Mvar"])
            out_file.write(",")
            out_file.write(record["IPload_MW"])
            out_file.write(",")
            out_file.write(record["IQload_Mvar"])
            out_file.write(",")
            out_file.write(record["YPload_MW"])
            out_file.write(",")
            out_file.write(record["YQload_Mvar"])
            out_file.write(",")
            out_file.write(record["owner_num"])
            out_file.write(",")
            out_file.write(str(int(record["scalable"])))
            # out_file.write(record["scalable"])  
            out_file.write(",")
            out_file.write(str(int(record["interruptible"])))
            # out_file.write(record["interruptible"])  

            out_file.write("\n")
    out_file.write("0 \n")  # End Load data, Begin Fixed shunt
    out_file.write("0 \n")  # End Fixed shunt data, Begin Generator

    for record in data:
        # each record is now a python object
        if (
            record["type"] == "generator-data"
            and (record["name"].split()[0]).lower() == "gen"
        ):
            out_file.write(record["Bus_Number"])
            out_file.write(",")
            out_file.write("'" + record["gen_id"]+ "'")  
            out_file.write(",")
            out_file.write(record["PGen_MW"])
            out_file.write(",")
            out_file.write(record["QGen_Mvar"])
            out_file.write(",")
            out_file.write(record["QMax_Mvar"])
            out_file.write(",")
            out_file.write(record["QMin_Mvar"])
            out_file.write(",")
            out_file.write(record["VSched_pu"])
            out_file.write(",")
            out_file.write(record["Remote_Bus"])
            out_file.write(",")
            out_file.write(record["Mbase_MVA"])
            out_file.write(",")
            out_file.write(record["R_Source_pu"])
            out_file.write(",")
            out_file.write(record["X_Source_pu"])
            out_file.write(",")
            out_file.write(record["RTran_pu"])
            out_file.write(",")
            out_file.write(record["XTran_pu"])
            out_file.write(",")
            out_file.write(record["Gentap_pu"])
            out_file.write(",")
            out_file.write(str(int(record["in_service"])))
            # out_file.write(record["in_service"])
            out_file.write(",")
            out_file.write(record["rmpct"])
            out_file.write(",")
            out_file.write(record["PMax_MW"])
            out_file.write(",")
            out_file.write(record["PMin_MW"])
            out_file.write(",")
            out_file.write("\n")

    out_file.write("0 \n")  # End generator data, Begin branch

    for record in data:
        # each record is now a python object
        if (
            record["type"] == "branch-data"
            and (record["name"].split()[0]).lower() == "branch"
        ):
            out_file.write(record["from_bus_number"])
            out_file.write(",")
            out_file.write(record["to_bus_number"])
            out_file.write(",")
            out_file.write("'" + record["branch_id"] + "'")
            out_file.write(",")
            out_file.write(record["line_r"])
            out_file.write(",")
            out_file.write(record["line_x"])
            out_file.write(",")
            out_file.write(record["charging_b"])
            out_file.write(",")
            out_file.write(record["rate_1"])
            out_file.write(",")
            out_file.write(record["rate_2"])
            out_file.write(",")
            out_file.write(record["rate_3"])
            out_file.write(",")
            out_file.write(record["line_g_from"])
            out_file.write(",")
            out_file.write(record["line_b_from"])
            out_file.write(",")
            out_file.write(record["line_g_to"])
            out_file.write(",")
            out_file.write(record["line_b_to"])
            out_file.write(",")
            out_file.write(str(int(record["in_service"])))
            # out_file.write(record["in_service"])
            out_file.write(",")
            out_file.write(record["length"])
            out_file.write(",")
            out_file.write(record["owner_1"])
            out_file.write(",")
            out_file.write(record["fraction_1"])

            out_file.write("\n")

    out_file.write("0 \n")  # End branch data, Begin Transformer datadata
    out_file.write("0 \n")  # End Transformer data, Begin Area interchange

    out_file.write("0 \n")  # End Area interchange data, Begin Two terminal DC
    out_file.write("0 \n")  # End Two terminal DC data, Begin Voltage source converter
    out_file.write("0 \n")  # End Voltage src converter Begin Impedance correction
    out_file.write("0 \n")  # End Impedance correction data, Begin Multi-terminal DC
    out_file.write("0 \n")  # End Multi-terminal DC data, Begin Multi-section line
    out_file.write("0 \n")  # End Multi-section line data, Begin Zone

    out_file.write("0 \n")  # End Zone data, Begin Inter-area transfer
    out_file.write("0 \n")  # End Zone data, Begin Owner

    out_file.write("0 \n")  # End Owner data, Begin FACTS device
    out_file.write("0 \n")  # End FACTS device data, Begin Switched shunt

    out_file.write("0 \n")  # End Switched shunt data, Begin GNE device
    out_file.write("0 \n")  # End GNE device data, Begin Induction machine
    out_file.write("0 \n")  # End Induction machine
    out_file.write("Q \n")  # End file
    print("Done")
