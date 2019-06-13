# Load RUCKUS environment and library
source -quiet $::env(RUCKUS_DIR)/vivado_proc.tcl

# Load source code
loadSource           -dir "$::DIR_PATH/rtl"
loadSource -sim_only -dir "$::DIR_PATH/tb"
loadIpCore           -dir "$::DIR_PATH/ip"
loadConstraints      -dir "$::DIR_PATH/xdc"
